from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Subquery, OuterRef, Q
from django.views.generic import View
from django.template.loader import render_to_string, get_template
from PyPDF3 import PdfFileWriter, PdfFileReader

from .models import myEvents, pickedupEvent
from profiles.models import userProfile

from django.core.exceptions import ObjectDoesNotExist
import qrcode
import qrcode.image.svg

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.lib.pagesizes import A4, landscape
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize

from .utils import render_to_pdf

from io import BytesIO
import requests


@login_required
def list_event(request):
    datas = myEvents.objects.all()
    return render(request, 'events/index.html',{'datas':datas})


@login_required
def profile_event(request):
    user = request.user
    
    if request.user.is_superuser:
        datas = myEvents.objects.all()
    else:
        # datas = myEvents.objects.all().annotate(status=Subquery(pickedupEvent.objects.filter(participant_id=user.pk).values('status')))
        # print(datas)
        datas = pickedupEvent.objects.select_related('participant','event').filter(participant__user__username=user)
        
    return render(request, 'events/event_profile.html', {'datas':datas})


def active_events(request):
    events = myEvents.objects.filter(tgl_acara__gte=timezone.now())
    
    return render(request, 'events/active_events.html', {'events':events})

@login_required
def detail_event(request, pk):
    obj = get_object_or_404(myEvents, pk=pk)
    
    # user_id = request.user.pk
    user_id = userProfile.objects.get(user=request.user)
    
    if obj.tgl_acara < timezone.now():
        
        messages.error(request,"Event ini sudah lewat!")
        
    datas = myEvents.objects.all().filter(pk=pk).annotate(status=Subquery(pickedupEvent.objects.filter(event_id=OuterRef('pk'),participant__user__username=user_id).values('status'))).annotate(uid=Subquery(pickedupEvent.objects.filter(event_id=OuterRef('pk'),participant__user__username=user_id).values('uid')))
    
    return render(request, 'events/detail_event.html', {'obj':obj,'datas':datas})

@login_required
def event_front(request):
    obj = myEvents.objects.all()
    
    return render(request, 'informations.html',{'obj':obj})


def register_event(request):
    user = request.POST['user_id']
    pk = request.POST['event_id']
    
    user_id = userProfile.objects.get(user__pk=user)
    my_event = myEvents.objects.get(pk=pk)
    # pk = myEvents.objects.get(pk=pk)
    # user = request.user
    # if request.method == 'POST':
    cek = pickedupEvent.objects.select_related('participant','event').filter(participant_id=user_id.pk,event_id=pk)
    if cek.exists():
        return JsonResponse({'msg':'exist'})
    else:
        data = pickedupEvent.objects.create(participant_id=user_id.pk, event_id=my_event.pk, status=True)
        
    uid = cek[0].uid
    
    pesan = f"""
    Anda berhasil terdaftar sebagai peserta
    <b>{my_event.nama_event}</b>

    Tgl/Jam : {my_event.tgl_acara.date()}/{my_event.tgl_acara.time()}

    Detail : <a href="http://localhost:8000/events/{uid}/event/">Klik Disini</a>
    """
    API_KEY = '5644982761:AAEVn3itxbBw2a3N9kjjDr29mxkpW34RaU4'
    hp = user_id.id_telegram
    url = f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={user_id.id_telegram}&parse_mode=html&text={pesan}"
    print(requests.get(url).json())
    return JsonResponse({'msg':'success'})

def detail_event_uid(request, uuid):
    try:
        data = pickedupEvent.objects.select_related('participant','event').get(uid=uuid)
        
        # if datas.DoesNotExist:
        #     messages.error(request, 'Alamat anda salah!')
        context = {
            'data':data
        }
        return render(request, 'events/detail_event_uid.html', context)
    except ObjectDoesNotExist:
        messages.error(request,"HAHAHAH")
        # data = pickedupEvent.objects.select_related('participant','event').get(uid=uuid)
        return redirect('/')

def name_tag(request, pk):
    datas = pickedupEvent.objects.select_related('event','participant').filter(participant__user__username=request.user, event=pk)[0]
    data = [datas.event.nama_event, datas.participant.nama, datas.participant.nama_perusahaan,
        datas.join_date, datas.status]
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(data, iamge_factory=factory, box_size=60)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()

    context = {
        'data':data,
        'svg':svg
    }

    return render(request, 'events/name_tag.html',context)

def certificate(request,pk):
    data = pickedupEvent.objects.select_related('participant','event').filter(participant__user__username=request.user, event__id=pk)
    if not data.exists():
        messages.error(request,"Anda tidak pernah mengikuti event ini")
    context = {
        'data':data
    }
    return render(request, 'events/certificate.html',context)

class GenerateSertifikat(View):
    def get(self, request, pk, *args, **kwargs):
        data = pickedupEvent.objects.select_related('participant','event').filter(participant__user__username=request.user, uid=pk)
        if not data.exists():
            return redirect('detail-event', pk=data[0].event.pk)

        for d in data:
            sumber = [d.event.narasumber, "DEPUTI DIREKTUR KANWIL SUMBAGUT"]
        print(data[0].event.sertifikat.url)
            
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(sumber, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        svg = stream.getvalue().decode()
        template = get_template('events/certificate.html')
        context = {
            'data':data,
            'svg':svg
        }
        html = template.render(context)
        # print(html)

        pdf = render_to_pdf(html)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Sertifikat.pdf"
            content = "inline; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response

        return HttpResponse("NOT FOUND!")
            

def certificate_view(request,pk):
    data = pickedupEvent.objects.select_related('participant','event').filter(participant__user__username=request.user, uid=pk)
    if not data.exists():
        messages.error(request,"Anda tidak pernah mengikuti event ini")
    context = {
        'data':data
    }
    return render(request, 'events/certificate.html',context)

def genCert(request,pk):
    data = pickedupEvent.objects.select_related('participant','event').filter(participant__user__username=request.user, uid=pk)
    # print(data[0].event.sertifikat.path)
    pw = defaultPageSize[0]
    ph = defaultPageSize[1]
    if data.exists():
        pack = BytesIO()
        can = canvas.Canvas(pack, pagesize=landscape(A4))
        can.setFont("Helvetica",60)
        nama = data[0].participant.nama
        # tw = stringWidth(data[0].participant.nama,"Helvetica",60)
        nw = stringWidth(nama,"Helvetica",60)
        r1 = (pw-nw)/2.0
        
        # spasi = len((data[0].participant.nama).split(' '))
        spasi = len(nama.split(' '))
        x,y = (200, 265)
        if r1 < 0 :
            can.drawString(x + (pw-nw),y,nama)
        elif r1 > 100 and r1 < 200:
            can.drawString(x + (r1/2), y, nama)
        elif r1 > 0 and r1 < 100:
            can.drawString(x - (r1/2),y,nama)
        else:
            can.drawString(x+(r1*0.7),y,nama)
        
        ew = stringWidth(data[0].event.nama_event, "Helvetica", 20)
        r2 = (pw-ew)/2.0
        can.setFont("Helvetica",20)
        # print(r2)
        if r2 < 0 :
            can.drawString(x + r2,240,data[0].event.nama_event)
        elif r2 > 100 and r2 < 145:
            can.drawString(x - r2, 240, data[0].event.nama_event)
        elif r2 > 145 and r2 < 200:
            can.drawString(300, 240, data[0].event.nama_event)
        elif r2 > 0 and r2 < 100:
            can.drawString(x + (r2*0.2),240,data[0].event.nama_event)
        else:
            can.drawString(x+(r2*0.7),240,data[0].event.nama_event)

        sw = stringWidth(data[0].event.narasumber,"Helvetica",16)
        can.setFont("Helvetica",16)
        r3 = (pw-sw) / 2.0
        # print(r3)

        if r3 < 0 :
            can.drawString(x + r3,160,data[0].event.narasumber)
        elif r3 > 100 and r3 < 145:
            can.drawString(x - r3, 160, data[0].event.narasumber)
        elif r3 > 145 and r3 < 200:
            can.drawString(300, 160, data[0].event.narasumber)
        elif r3 > 0 and r3 < 100:
            can.drawString(x + (r3*0.2),160,data[0].event.narasumber)
        else:
            can.drawString(x+(r3*0.7),160,data[0].event.narasumber)

        jw = stringWidth("Asisten Deputi Direktur Kepesertaan","Helvetica",12)
        can.setFont("Helvetica",12)
        r4 = (pw-sw) / 2.0
        print(r4)

        if r4 < 0 :
            can.drawString(x + r4,140,"Asisten Deputi Direktur Kepesertaan")
        elif r4 > 100 and r4 < 145:
            can.drawString(x - r4, 140, "Asisten Deputi Direktur Kepesertaan")
        elif r4 > 145 and r4 < 200:
            can.drawString(300, 140, "Asisten Deputi Direktur Kepesertaan")
        elif r4 > 0 and r4 < 100:
            can.drawString(x + (r4*0.2),140,"Asisten Deputi Direktur Kepesertaan")
        else:
            can.drawString(x+(r4*0.56),140,"Asisten Deputi Direktur Kepesertaan")

        can.save()
        pack.seek(0)
        new_pdf = PdfFileReader(pack)
        exist_pdf = PdfFileReader(open(data[0].event.sertifikat.path,"rb"))
        print(exist_pdf)
        output = PdfFileWriter()
        page = exist_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        outputStream = open("media/events/sertifikat/final.pdf","wb")

        response = HttpResponse(content_type='application/pdf')
        filename = "Sertifikat %s - %s .pdf" % (data[0].event.nama_event, data[0].participant.nama)
        content = "inline; filename=%s" % (filename)
        response['Content-Disposition'] = content

        output.write(response)
        outputStream.close()
        
        return response