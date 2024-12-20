from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    anio_fundacion = models.IntegerField()

    def __str__(self):
        return self.nombre
    
class Genero(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)
    autor = models.CharField(max_length=200)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    generos = models.ManyToManyField(Genero)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.nombre
    

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UsuarioManager(models.Manager):
    def create_user(self, email, password=None, role=None):

        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado')
        usuario = self.model(email=email, role=role)
        usuario.password = make_password(password)
        usuario.save(using=self._db)
        return usuario

class Usuario(models.Model):
    ROLES_CHOICES = [
        ('jefe_bodega', 'Jefe de Bodega'),
        ('bodeguero', 'Bodeguero'),
    ]
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLES_CHOICES)

    objects = UsuarioManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.email} ({self.role})"

class Credenciales(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Usuario.ROLES_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.email} - {self.role}'

    class Meta:
        db_table = 'credenciales'


class Informe(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    enviado_a = models.EmailField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.titulo
    
