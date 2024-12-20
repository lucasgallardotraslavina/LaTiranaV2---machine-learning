from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import connection


from Aplicacion.models import Informe, Usuario, Credenciales, Libro, Genero
from Aplicacion.forms import FormLibro, EditorialForm, GeneroForm, InformeForm



def index(request):
    return render(request, 'Aplicacion/indexs/index.html')

#====================================================================================
#==============================Funcniones Acceso=====================================
#====================================================================================

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.verify_password(password):
                user = authenticate(request, username=usuario.email, password=password)
                if user is None:
                    user = Usuario.objects.create_user(
                        email=usuario.email, 
                        password=password
                    )
                login(request, user)
                if usuario.role == 'jefe_bodega':
                    return redirect('dashboard_jefe_bodega')
                elif usuario.role == 'bodeguero':
                    return redirect('dashboard_bodeguero')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo no está registrado.')
    return render(request, 'Aplicacion/login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('register')
        usuario = Usuario.objects.create_user(email=email, password=password, role=role)
        credenciales = Credenciales.objects.create(usuario=usuario, role=role)
        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('login')
    return render(request, 'Aplicacion/register.html')

#====================================================================================
#==============================Funcniones bodeguero==================================
#====================================================================================

def bodeguero_dashboard(request):
    return render(request, 'Aplicacion/indexs/index_bodeguero.html')

#====================================================================================
#==============================Funcniones Catalogos==================================
#====================================================================================
def catalogo_busqueda(request):
    query = request.GET.get('q', '')
    if query:
        libros = Libro.objects.filter(titulo__icontains=query)
    else:
        libros = Libro.objects.all()
    return render(request, 'catalogo.html', {'libros': libros})

def ficcion(request):
    return render(request, 'Aplicacion/generos/ficcion.html')

#====================================================================================
#==============================Funcniones Informe====================================
#====================================================================================
def informes(request):
    form = InformeForm()
    if request.method == 'POST':
        form = InformeForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            observaciones = form.cleaned_data.get('observaciones', '')
            destinatario = form.cleaned_data['destinatario']
            usuario = request.user

            try:

                asunto = f"Informe: {titulo}"
                mensaje = f"Descripción: {descripcion}\n\nObservaciones: {observaciones}"
                email = EmailMessage(
                    asunto,
                    mensaje,
                    settings.EMAIL_HOST_USER,
                    [destinatario]
                )
                email.send()
                Informe.objects.create(
                    titulo=titulo,
                    contenido=descripcion,
                    enviado_a=destinatario,
                    observaciones=observaciones,
                    usuario=usuario
                )

                messages.success(request, "Informe enviado y guardado con éxito.")
                return redirect('informes')
            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {e}")
    return render(request, 'Aplicacion/informes/informes.html', {'form': form})


def informes_jefe(request):
    form = InformeForm()
    if request.method == 'POST':
        form = InformeForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            observaciones = form.cleaned_data.get('observaciones', '')
            destinatario = form.cleaned_data['destinatario']
            usuario = request.user

            try:
                asunto = f"Informe: {titulo}"
                mensaje = f"Descripción: {descripcion}\n\nObservaciones: {observaciones}"
                email = EmailMessage(
                    asunto,
                    mensaje,
                    settings.EMAIL_HOST_USER,
                    [destinatario]
                )
                email.send()
                Informe.objects.create(
                    titulo=titulo,
                    contenido=descripcion,
                    enviado_a=destinatario,
                    observaciones=observaciones,
                    usuario=usuario
                )

                messages.success(request, "Informe enviado y guardado con éxito.")
                return redirect('informes_jefe')
            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {e}")
    return render(request, 'Aplicacion/informes/informes_jefe.html', {'form': form})


def listar_informes(request):
    informes = Informe.objects.filter(usuario=request.user)
    return render(request, 'Aplicacion/informes/informes.html', {'informes': informes})

def informes_guardados(request):
    informes = Informe.objects.all()
    return render(request, 'Aplicacion/informes/informes_guardados.html', {'informes': informes})
 
#====================================================================================
#================================= Funciones Jefe ===================================
#====================================================================================
def jefe_bodega_dashboard(request):
    return render(request, 'Aplicacion/indexs/index_jefe_bodega.html')

def listadoLibros_jefe(request):
    libros = Libro.objects.all()
    data = {'libros': libros} 
    return render(request, 'Aplicacion/libros/libros_jefe.html', data) 

#====================================================================================
#============================== Funciones Libros=====================================
#====================================================================================

def libros(request):
    libros = Libro.objects.all()
    return render(request, 'Aplicacion/libros/libros.html', {'libros': libros})

def agregarLibro(request):
    form = FormLibro()
    if request.method == 'POST':
        form = FormLibro(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El libro se ha registrado con éxito!')
            form = FormLibro()
    return render(request, 'Aplicacion/libros/agregarLibro.html', {'form': form})

def agregarLibro_jefe(request):
    form = FormLibro()
    if request.method == 'POST':
        form = FormLibro(request.POST)
        if form.is_valid():
            form.save()
        return redirect('agregarLibro_jefe')
    data = {'form': form}   
    return render(request, 'Aplicacion/libros/agregarLibro_jefe.html', data)

def eliminarLibro(request, id):
    libro = Libro.objects.get(id=id)
    libro.delete()
    return redirect('libros') 

def actualizarLibro(request, id):
    libro = Libro.objects.get(id=id)
    form = FormLibro(instance=libro)
    if request.method == 'POST':
        form = FormLibro(request.POST, instance=libro)
        if form.is_valid():
            form.save()
        return redirect('libros')
    data = {'form': form}
    return render(request, 'Aplicacion/libros/agregarLibro.html', data)

def listado_libros(request):
    query = request.GET.get('q', '')
    libros = []

    try:
        with connection.cursor() as cursor:
            if query:
                cursor.callproc('buscar_libros', [query])
                libros = cursor.fetchall()
            else:
                cursor.callproc('buscar_libros', [''])
                libros = cursor.fetchall()
    except Exception as e:
        libros = []
        messages.error(request, f"Error al cargar los libros: {e}")

    
    libros = []
    for libro in libros:
        generos = libro[5]
        generos_lista = []
        if generos:
            generos_lista = [genero.strip() for genero in generos.split(',')]
            generos_lista = Genero.objects.filter(nombre__in=generos_lista)

        
        libros.append({
            'id': libro[0],
            'nombre': libro[1],
            'autor': libro[2],
            'descripcion': libro[3],
            'editorial': libro[4],
            'generos': generos_lista, 
            'cantidad': libro[6]
        })

    return render(request, 'Aplicacion/libros/libros.html', {'libros': libros})
#====================================================================================
#====================================================================================
#====================================================================================

def agregarEditorial(request):
    if request.method == 'POST':
        form = EditorialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Editorial agregada exitosamente.")
            return redirect('libros')
        else:
            messages.error(request, "Hubo un error en el formulario.")
    else:
        form = EditorialForm()

    return render(request, 'Aplicacion/editoriales y generos/agregarEditorial.html', {'form': form})

def agregarGenero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('libros')
    else:
        form = GeneroForm()

    return render(request, 'Aplicacion/editoriales y generos/agregarGenero.html', {'form': form})

#----------------------------------------

import io
import os
from keras.preprocessing import image
import numpy as np
from keras.models import load_model
from django.shortcuts import render

model = load_model(r'C:\Users\lucas\Desktop\LaTiranaV2 - machine learning\model.keras')


UPLOAD_DIR = r'C:\Users\lucas\Desktop\LaTiranaV2 - machine learning\media'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def classify_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        
        img = request.FILES['image']
        
        img_name = img.name
        
        
        image_path = os.path.join(UPLOAD_DIR, img_name)
        with open(image_path, 'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
        
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img) 
        img_array = np.expand_dims(img_array, axis=0) 
        img_array = img_array / 255.0 

        prediccion = model.predict(img_array)

        clases = ['animal', 'enemigo', 'herramientas']

        prediccion_index = np.argmax(prediccion, axis=1)[0]
        result = clases[prediccion_index]

        return render(request, 'Aplicacion/machine_learning.html', {
            'result': result,
            'uploaded_image_url': f'/media/{img_name}'
        })

    return render(request, 'Aplicacion/machine_learning.html')