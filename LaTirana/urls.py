from django.urls import path
from Aplicacion import views
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

#==============================================================================================
#============================================Acceso============================================
#==============================================================================================
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

    path('dashboard/jefe-bodega/', views.jefe_bodega_dashboard, name='dashboard_jefe_bodega'),
    path('dashboard/bodeguero/', views.bodeguero_dashboard, name='dashboard_bodeguero'),
#==============================================================================================
#============================================Libros============================================
#==============================================================================================
    path('libros_jefe/',views.listadoLibros_jefe, name='libros_jefe'),
    path('libros/', views.libros, name='libros'),
    path('agregarLibro/', views.agregarLibro, name='agregarLibro'),
    path('actualizarLibro/<int:id>/', views.actualizarLibro, name='actualizarLibro'),
    path('eliminarLibro/<int:id>/', views.eliminarLibro, name='eliminarLibro'),
    path('buscar/', views.catalogo_busqueda, name='catalogo_busqueda'),

    path('libross/', views.listado_libros, name='listado_libros'),
#==============================================================================================
#============================================Informes==========================================
#==============================================================================================
    path('informes/', views.informes, name='informes'), 
    path('informes_jefe/',views.informes_jefe, name='informes_jefe'),
    path('informes_guardados/', views.informes_guardados, name='informes_guardados'),
#==============================================================================================
#===============================Editoriales y Generos==========================================
#==============================================================================================
    path('agregarEditorial/', views.agregarEditorial, name='agregarEditorial'),
    path('agregarGenero/', views.agregarGenero, name='agregarGenero'),


    path('ficcion/', views.ficcion, name='ficcion'),
    path('machine_learning/', views.classify_image, name='machine_learning'),


] + static('/media/', document_root=r'C:\Users\lucas\Desktop\LaTiranaV2 - machine learning\media')  # Ajusta la ruta
