from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from random import randint
import os
import uuid
from django.conf import settings



# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

# def save_pdf(params:dict):
#     template=get_template('search_location_detail.html')
#     html=template.render(params)
#     response=BytesIO()
#     pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
#     file_name=uuid.uuid4()
#     try:
#         with open(str(settings.BASE_DIR)+f'/static/(file_name).pdf', 'wb+') as output:
#             pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
#     except Exception as e:
#         print(e)
        
#     if pdf.err:
#         return '', False
#     return file_name, True
            


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    #pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, encoding="ISO-8859-1")
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def render_to_file(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    file_name = "{0}.pdf".format(randint(1, 1000000))
    file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")),"media/temp", file_name)
    with open(file_path, 'wb') as pdf:
        pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
    return file_name