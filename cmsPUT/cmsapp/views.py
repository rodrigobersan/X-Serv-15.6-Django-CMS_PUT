from django.shortcuts import render
from django.http import HttpResponse
from models import WebPageDB
from django.views.decorators.csrf import csrf_exempt
import urllib

# Create your views here.

def fullurl(url):
    if url[0:4] == "www.":
        url = "http://" + url
    elif url[0:7] == "http://" and url[7:11] != "www.":
            url = url[0:7] + "www." + url[7:]
    elif url[0:8] == "https://" and url[8:12] != "www.":
            url = url[0:8] + "www." + url[8:]
    else:
        url = "http://www." + url
    return(url)

@csrf_exempt
def app(request, url):
    url = fullurl(url)
    if request.method == "GET":
        try:
            webpage = WebPageDB.objects.get(URL=url)
        except WebPageDB.DoesNotExist:
            return HttpResponse("La URL " + url + " no esta registrada en la base de datos")
        respuesta = showoneurl(request, url)

    if request.method == "PUT" or request.method == "POST":
        try:
            webpage = WebPageDB.objects.get(URL=url)
        except WebPageDB.DoesNotExist:
            htmlcode = urllib.urlopen(url)
            webpage = WebPageDB(URL=url, HTMLCode=strhtmlcode)#falla al guardar HTMLCode. Es un TypeError pero no entiendo de donde viene...
            webpage.save()
            respuesta = "Se agregado la pagina web " + webpage.URL + " a la base de datos."
        respuesta = "La url ya se encuentra registrada en la base de datos. Su identificador es " + str(webpage.id) + " y su codigo HTML es: " + str(webpage.HTMLCode)
    if request.method == "DELETE":
        try:
            webpage = WebPageDB.objects.get(URL=url)
        except WebPageDB.DoesNotExist:
            return HttpResponse("La pagina web que intentas borrar no esta registrada en la base de datos")
        webpage.delete()
        respuesta = "La entrada se ha borrado satisfactoriamente."
    return HttpResponse(respuesta)

def showoneident(request, ident):
    try:
        webpage = WebPageDB.objects.get(id=ident)
    except WebPageDB.DoesNotExist:
        return HttpResponse("No hay ninguna url almacenada con el identificador " + ident + ".")
    respuesta = "El identificador " + str(webpage.id) + " se corresponde con la url " + webpage.URL + ", cuyo codigo HTML es: " + str(webpage.HTMLCode)
    return HttpResponse(respuesta)

def showoneurl(request, url):
    try:
        webpage = WebPageDB.objects.get(URL=url)
    except WebPageDB.DoesNotExist:
        return HttpResponse("La url " + webpage.URL + " no esta registrada en la base de datos.")
    respuesta = "La url " + webpage.URL + " se identifica con el id " + str(webpage.id) + " y su codigo HTML es: " + str(webpage.HTMLCode)
    return (respuesta)

def showall(request):
    urls = WebPageDB.objects.all()
    respuesta = "<p>Listado de todas las paginas guardadas:</p><ul>"
    for url in urls:
        respuesta += '<li><a href="/' + str(url.id) + '">' + url.URL + '</a>'
    respuesta += "</ul>"
    return HttpResponse(respuesta)
