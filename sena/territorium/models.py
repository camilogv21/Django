from distutils.command.upload import upload
from email.policy import default
from django.db import models

# Create your models here.


class Usuario(models. Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=254)
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=254)
    roles = (
        ("R", "administrador"),
        ("I", "instructor"),
        ("A", "aprendiz"),

    )
    rol = models.CharField(choices= roles, max_length=1, default="A")
    foto = models.ImageField(upload_to = 'territorium/fotos', default = 'territorium/fotos/default.png')

    def __str__(self) :
        return self.nombre


class Aprendiz(models.Model):
    cedula = models.IntegerField()
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()


    def __str__(self):
        return self.nombre

class Monitoria(models.Model):
    cat = models.CharField(max_length=100)
    aprendiz = models.ForeignKey(Aprendiz, on_delete= models.DO_NOTHING) 
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()

    def __str__(self):
        return f"{self.cat}"

class Actividades(models.Model):
    monitoria = models.ForeignKey(Monitoria, on_delete= models.DO_NOTHING)
    actividad = models.CharField(max_length=254)
    observaciones = models.TextField()
    fecha = models.DateField(auto_now_add= True)

    def __str__(self):
        return f"{self.monitoria} -- {self.actividad}"

    