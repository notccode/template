from django.contrib import admin
from .models import Estudiantes, Cursos, Inscripcion
 
@admin.register(Estudiantes)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'email', 'fecha_registro']
    search_fields = ['rut', 'nombre', 'email']
    list_filter = ['fecha_registro']
   
@admin.register(Cursos)
class CursosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'activo']
    search_fields = ['id', 'nombre']
   
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['id', 'curso_id', 'estudiante_id', 'fecha_inscripcion']
    search_fields = ['id', 'curso_id', 'estudiante_id']
 



