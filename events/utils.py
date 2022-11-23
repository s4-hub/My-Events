from io import BytesIO, StringIO
from PyPDF3 import PdfFileWriter, PdfFileReader
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize

def render_to_pdf(src):
    # template = get_template(template_src)
    # print(template)
    # html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(src.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None

def pdf_rendering(file, text, **kwargs):
    pw = defaultPageSize[0]
    ph = defaultPageSize[1]
    
    tw = stringWidth(text,"Helvetica", 60)
    pack = BytesIO()
    can = canvas.Canvas(pack, pagesize=landscape(A4))
    can.setFont("Helvetica", 60)
    print(pw - tw)
    y = 265
    pdf_ = can.beginText((pw - tw) / 2.0 , y)
    pdf_.textOut(text)
    # pos x = 200 s.d 615, y = 265
    x = 200
    if(pw - tw) < 0:
        can.drawString(x+(pw - tw)/2.0,y,text)
    elif(pw - tw) > 100 and (pw - tw) < 200:
        can.drawString(x, y, text)
    else:
        can.drawString(x-(pw-tw)/2.0, y, text)
    # print(cur_x)
    # if len(nama) == 16:
    #     can.drawString(x ,265,nama)
    # elif len(nama) > 16:
    #     can.drawString(x-(cur_x*3),265, nama)
    # else : 
    #     can.drawString(x+cur_x, 265, nama)
    can.save()

    pack.seek(0)

    new_pdf = PdfFileReader(pack)
    exist_pdf = PdfFileReader(open(file,"rb"))
    output = PdfFileWriter()
    page = exist_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = open("final.pdf","wb")
    output.write(outputStream)
    outputStream.close()




