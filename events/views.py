from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Subquery, OuterRef, Q
from django.views.generic import View
from django.template.loader import render_to_string, get_template

from .models import myEvents, pickedupEvent
from profiles.models import userProfile

from django.core.exceptions import ObjectDoesNotExist
import qrcode
import qrcode.image.svg

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

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
    user_id = userProfile.objects.get(user__username=request.user)
    
    if obj.tgl_acara < timezone.now():
        
        messages.error(request,"Event ini sudah lewat!")
        
    datas = myEvents.objects.filter(pk=pk).annotate(status=Subquery(pickedupEvent.objects.filter(event_id=OuterRef('pk'),participant_id=user_id).values('status')))
        
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
            
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(sumber, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        svg = stream.getvalue().decode()
        template = get_template('events/certicate.html')
        context = {
            'data':data,
            'svg':svg
        }
        html = template.render(context)

        pdf = render_to_pdf(html)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Sertifikat %s - %s.pdf" % (data[0].event.nama_event, data[0].participant.nama)
            content = "inline; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response

        return HttpResponse("NOT FOUND!")
            

def certificate_view(request):
    return render(request, 'events/certificate2.html')