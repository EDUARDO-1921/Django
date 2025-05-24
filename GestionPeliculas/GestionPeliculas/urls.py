from django.contrib import admin
from django.urls import path
from appPeliculas import views
from django.conf import settings
from django.conf.urls.static import static

# Importa la vista que usarás
from appPeliculas.views import inicio, agregarGenero

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', views.inicio, name='inicio'),
    path('agregarGenero/', views.agregarGenero),
    path('vistaAgregarGenero/', views.vistaAgregarGenero),
    path('listarPeliculas/', views.listarPeliculas),
    path('agregarPelicula/', views.agregarPelicula,),
    path('vistaAgregarPelicula/', views.vistaAgregarPelicula,),
  path('consultarPelicula/<int:id>/', views.consultarPeliculaPorId,),
  path('actualizarPelicula/', views.actualizarPelicula),
  path('eliminarPelicula/<int:id>/', views.eliminarPelicula),

]

# Sólo en DEBUG sirve los archivos media
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

