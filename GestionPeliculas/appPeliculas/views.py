from django.conf import settings
from django.shortcuts import render, redirect    
from django.db import Error
from appPeliculas.models import Genero, Pelicula
from django.http import JsonResponse, HttpResponse 
from django.views.decorators.csrf import csrf_exempt
import os

def inicio(request):
    """
    Muestra la página de inicio.
    Asegúrate de tener un archivo
    appPeliculas/templates/inicio.html
    """
    return render(request, "inicio.html")



@csrf_exempt
def agregarGenero(request):
    try:
        # recibir el nombre del género en una variable local
        nombre = request.POST['txtNombre']

        # crear objeto de tipo Genero
        genero = Genero(genNombre=nombre)

        # guardar el objeto en la base de datos
        genero.save()

        mensaje = "Género agregado correctamente"
    except Error as error:
        mensaje = str(error)

    retorno = {"mensaje": mensaje}
    #return JsonResponse(retorno)
    return render(request, "agregarGenero.html",retorno)


def vistaAgregarGenero(request):
    return render(request,"agregarGenero.html")

def listarPeliculas(resquest):
    Peliculas =Pelicula.objects.all().values()
    print(Peliculas)
    retorno= {"peliculas":list(Peliculas)}
    return JsonResponse(retorno, content_type='application/json')

def listarPeliculas(request):
    peliculas = Pelicula.objects.all()
    print(peliculas)  # para revisar en la consola
    retorno = {"peliculas": peliculas}
    #retorno JsonResponse (retorno, content_type='aplication')
    return render(request, "listarPeliculas.html", retorno)

@csrf_exempt
def agregarPelicula(request):
    try:
        codigo       = request.POST['txtCodigo']
        titulo       = request.POST['txtTitulo']
        protagonista = request.POST['txtProtagonista']
        duracion     = int(request.POST['txtDuracion'])
        resumen      = request.POST['txtResumen']
        foto         = request.FILES['fileFoto']
        idGenero     = int(request.POST['cbGenero'])
        genero       = Genero.objects.get(pk=idGenero)

        pelicula = Pelicula(
            pelCodigo       = codigo,
            pelTitulo       = titulo,
            pelProtagonista = protagonista,
            pelDuracion     = duracion,
            pelResumen      = resumen,
            pelFoto         = foto,
            pelGenero       = genero
        )
        pelicula.save()
        mensaje = "Película agregada correctamente"
    except Exception as error:
        mensaje = str(error)

    retorno = {'mensaje': mensaje, 'idPelicula': pelicula.id}
    return JsonResponse(retorno)

def vistaAgregarPelicula(request):
    generos = Genero.objects.all()
    retorno = {"generos": generos}
    return render(request, "agregarPelicula.html", retorno)

def consultarPeliculaPorId(request, id):
   pelicula = Pelicula.objects.get(pk=id)
   generos  = Genero.objects.all()
    # 3) Preparar el contexto y renderizar el formulario de actualización
   retorno = {"pelicula": pelicula,"generos" : generos}
   return render(request, "actualizarPelicula.html", retorno)

def actualizarPelicula(request):
    try:
        idPelicula = request.POST['idPelicula']
        # obtener la pelicula a partir de su id
        peliculaActualizar = Pelicula.objects.get(pk=idPelicula)
        # actualizar los campos
        peliculaActualizar.pelCodigo = request.POST['txtCodigo']
        peliculaActualizar.pelTitulo = request.POST['txtTitulo']  # Corregido de pelIitulo a pelTitulo
        peliculaActualizar.pelProtagonista = request.POST['txtProtagonista']
        peliculaActualizar.pelDuracion = int(request.POST['txtDuracion'])
        peliculaActualizar.pelResumen = request.POST['txtResumen']
        idGenero = int(request.POST['cbGenero'])
        # obtener el objeto Genero a partir de su id
        genero = Genero.objects.get(pk=idGenero)
        peliculaActualizar.pelGenero = genero
        foto = request.FILES.get('fileFoto')  # Corregido de filefoto a fileFoto (mayúscula)
        
        # si han enviado foto se actualiza el campo
        if foto:
            # primero eliminamos la foto existente
            if peliculaActualizar.pelFoto:  # Verificación adicional para evitar errores
                os.remove(os.path.join(settings.MEDIA_ROOT, str(peliculaActualizar.pelFoto)))
            # actualizamos con la nueva foto
            peliculaActualizar.pelFoto = foto  # Corregido de pelfoto a pelFoto (mayúscula)
        
        # actualizar la pelicula en la base de datos
        peliculaActualizar.save()
        mensaje = "Película Actualizada"
    except Exception as error:  # Cambiado de Error a Exception para mayor cobertura
        mensaje = str(error)
    
    retorno = {'mensaje': mensaje}
    #return JsonResponse(retorno)
    return redirect("/listarPeliculas")

def eliminarPelicula(request, id):
    try:
        peliculaAEliminar = Pelicula.objects.get(pk=id)
        peliculaAEliminar.delete()
        mensaje= "Pelicula Eliminada Correctamente"
        return redirect('/listarPeliculas')
    except Exception as error:
        mensaje=str(error)
        retorno={"mensaje":mensaje}
        