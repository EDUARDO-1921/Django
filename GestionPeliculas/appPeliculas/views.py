# appPeliculas/views.py
from django.shortcuts import render
from django.db import Error
from appPeliculas.models import Genero, Pelicula
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    return render(request, "agregarGenero.html")


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
    return render(request, "listarPeliculas.html", retorno)


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
    # 1) Obtener la película con ese ID
    pelicula = Pelicula.objects.get(pk=id)
    # 2) Obtener todos los géneros (para rellenar el <select>)
    generos  = Genero.objects.all()
    # 3) Preparar el contexto y renderizar el formulario de actualización
    retorno = {"pelicula": pelicula,"generos" : generos}
    return render(request, "actualizarPelicula.html", retorno)