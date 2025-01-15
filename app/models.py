from django.db import models

from datetime import datetime
from django.db import models
 
class Cursos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=500)
    fecha_inicio = models.DateTimeField(default=datetime.now)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
   
class Inscripcion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_inscripcion = models.DateTimeField(default=datetime.now)
    curso = models.ForeignKey('Cursos', on_delete=models.CASCADE)
    estudiante = models.ForeignKey('Estudiantes', on_delete=models.CASCADE)

 
class Estudiantes(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=200)
    fecha_registro = models.DateTimeField(default=datetime.now)
 