from datetime import datetime
from enum import UNIQUE
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
import json
from django.http import JsonResponse
from django.urls import reverse
from .models import Cursos, Estudiantes
from django.core import serializers

def generar_menu(user: AbstractBaseUser | AnonymousUser):
    menu = []
    if user != None and user.is_authenticated:
        menu.append({'url':'/', 'nombre':'Home'})
        menu.append({'url':'/mensajes/', 'nombre':'Implementación mensajes 100%'})
        menu.append({'url':'/crud/', 'nombre':'Crud registro 0%'})
        menu.append({'url':'/busqueda/', 'nombre':'Buscar registros 0%'})
        menu.append({'url':'/detalle/', 'nombre':'Maestro detalle 0%'})

        menu.append({'url':'/mest/', 'nombre':'Mantenedor estudiantes'})
        menu.append({'url':'/mcur/', 'nombre':'Mantenedor cursos'})

    return menu

def mantenedor_estudiantes(request: HttpRequest):
    titulo = 'Mantenedor Estudiantes'

    listado = Estudiantes.objects.all()

    return render(request, "app/ges-lista-estudiantes.html", {'titulo':titulo ,'menu': generar_menu(request.user), 'listado':listado})

def mantenedor_cursos(request: HttpRequest):
    titulo = 'Mantenedor Cursos'
    listado = Cursos.objects.all()
    return render(request, "app/ges-lista-cursos.html", {'titulo':titulo ,'menu': generar_menu(request.user), 'listado':listado})

def estudiante(request: HttpRequest):
 
    titulo = 'Estudiante'
    accion = ''
    base = None
    message = None
    try:
        
        data = {'rut':'','nombre':'','email':''} 
        if request.method == "GET":
            
            accion = request.GET.get('accion')
            data['rut'] = request.GET.get('rut', '')
            data['nombre'] = request.GET.get('nombre', '')
            data['email'] = request.GET.get('email', '')
            if accion == 'editar' or accion == 'eliminar':  #preparar la accion editar
                estudiante = Estudiantes.objects.get(pk=data['rut'])
            else: #preparar la accion nuevo usuario
                estudiante = Estudiantes()
                estudiante.nombre = ""
                estudiante.rut = ""
                estudiante.email = ""
        
        else: #POST
            accion = request.POST.get('accion')
            print("POST")
            print(accion)
            print(request.POST.get('rut'))
            data['rut'] = request.POST.get('rut')
            data['nombre'] = request.POST.get('nombre')
            data['email'] = request.POST.get('email')
            if accion == 'editar': #ejecuta la accion editar
                estudiante = Estudiantes.objects.get(pk=data['rut'])
                estudiante.nombre = data['nombre']
                estudiante.rut = data['rut']
                estudiante.email = data['email']
                estudiante.save()
                base = toastOk('El estudiante se modificó correctamente')
            elif accion == 'eliminar':  #ejecuta la accion eliminar
                estudiante = Estudiantes.objects.get(pk=data['rut'])
                estudiante.delete()
                estudiante.rut = ""
                estudiante.nombre = ""
                estudiante.email = ""
                accion = 'crear'
                base = toastOk('El estudiante se eliminó correctamente')
                
                #lindo parche
            else: #ejecuta la accion nuevo
                estudiante = Estudiantes.objects.create(nombre=data['nombre'], rut=data['rut'], email=data['email'])
                estudiante.rut = ""
                estudiante.nombre = ""
                estudiante.email = ""
                base = toastOk('El estudiante se creós correctamente')
                #lindo parche

        if estudiante.fecha_registro != None:
            data['fecha_registro'] = estudiante.fecha_registro.isoformat()
        data['rut'] = estudiante.rut
        data['nombre']= estudiante.nombre
        data['email'] = estudiante.email
        
    except IntegrityError as ex:  # Catch IntegrityError for unique constraint violation
        base = toastError('El estudiante ya existe')
    except Estudiantes.DoesNotExist:  # Catch case where the student is not found (in 'editar' or 'eliminar')
        base = toastError('Estudiante no encontrado')


    return render(request, 'app/estudiante.html', {'accion': accion, 'titulo':titulo,'estudiante': data, 'base': base,'menu': generar_menu(request.user)}) 

def curso(request: HttpRequest):

    titulo = 'Curso'
    accion = ''
    base = None
    message = None
    try:
        
        data = {'id':'','nombre':'','descripcion':'','fecha_inicio':'','fecha_fin':'','activo':''} 
        if request.method == "GET":
            
            accion = request.GET.get('accion')
            data['id'] = request.GET.get('id', '')
            data['nombre'] = request.GET.get('nombre', '')
            data['descripcion'] = request.GET.get('descripcion', '')
            data['fecha_inicio'] = request.GET.get('fecha_inicio', '')
            data['fecha_fin'] = request.GET.get('fecha_fin', '')
            data['activo'] = request.GET.get('activo') == "on"

            if accion == 'editar' or accion == 'eliminar':  #preparar la accion editar
                curso = Cursos.objects.get(pk=int(data['id']))
            else: #preparar la accion nuevo usuario
                curso = Cursos()
                curso.id = 0
                curso.nombre = ""
                curso.descripcion = ""
                curso.fecha_inicio = None
                curso.fecha_fin =  None
                curso.activo = False
        
        else: #POST
            accion = request.POST.get('accion')
            data['id'] = request.POST.get('id', '')
            data['nombre'] = request.POST.get('nombre', '')
            data['descripcion'] = request.POST.get('descripcion', '')
            data['fecha_inicio'] = request.POST.get('fecha_inicio', '')
            data['fecha_fin'] = request.POST.get('fecha_fin', '')
            data['activo'] =  request.POST.get('activo') == "on"
            if accion == 'editar': #ejecuta la accion editar
                curso = Cursos.objects.get(pk=int(data['id']))
                curso.nombre = data['nombre']
                curso.id = int(data['id'])
                curso.descripcion = data['descripcion']
                curso.fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
                curso.fecha_fin = datetime.fromisoformat(data['fecha_fin'])
                curso.activo = data['activo']
                curso.save()
                base = toastOk('El curso se modificó correctamente')
            elif accion == 'eliminar':  #ejecuta la accion eliminar
                curso = Cursos.objects.get(pk=data['id'])
                curso.delete()
                curso.id = 0
                curso.nombre = ""
                curso.descripcion = ""
                curso.fecha_inicio = None
                curso.fecha_fin =  None
                curso.activo = False
                accion = 'crear'
                base = toastOk('El curso se eliminó correctamente')
                
                #lindo parche
            else: #ejecuta la accion nuevo
                Cursos.objects.create(nombre=data['nombre'], descripcion=data['descripcion'], fecha_inicio=datetime.fromisoformat(data['fecha_inicio']), fecha_fin=datetime.fromisoformat(data['fecha_fin']), activo= data['activo'])
                curso = Cursos()
                curso.id = 0
                curso.nombre = ""
                curso.descripcion = ""
                curso.fecha_inicio = None
                curso.fecha_fin =  None
                curso.activo = False
                accion = 'crear'
                base = toastOk('El curso se creós correctamente')
                #lindo parche
 
        if curso.fecha_inicio != None:
            data['fecha_inicio'] = curso.fecha_inicio 
        data['id'] = str(curso.id)
        data['nombre']= curso.nombre
        data['descripcion'] = curso.descripcion
        
        if curso.fecha_inicio == None:
            data['fecha_inicio'] = ''
        else:
            data['fecha_inicio'] = curso.fecha_inicio 
        if curso.fecha_fin == None:
            data['fecha_fin'] = ''
        else:
            data['fecha_fin'] = curso.fecha_fin
        data['activo'] = curso.activo
        
    except IntegrityError as ex:  # Catch IntegrityError for unique constraint violation
        base = toastError('El nombre del curso ya existe')
    except Cursos.DoesNotExist:  # Catch case where the student is not found (in 'editar' or 'eliminar')
        base = toastError('Curso no encontrado')
 

    return render(request, 'app/curso.html', {'accion': accion, 'titulo':titulo,'curso': data, 'base': base,'menu': generar_menu(request.user)}) 

def home(request: HttpRequest):
    titulo = 'Home'
    return render(request, "app/home.html", {'titulo':titulo ,'menu': generar_menu(request.user)})

def mensajes(request: HttpRequest):
    titulo = 'Funcionalidad mensajes WEB'
    base=''
    opcion = request.GET.get("opcion")
    if opcion == "eliminar":
        base = toastOk('El registro se ha eliminado correctamente')
    if opcion == "crea_ok":
       base = toastOk('El registro se ha eliminado correctamente')
    if opcion == "crea_error":
        base = toastError('Error al eliminar el registro por pagos asociados')
    if opcion == "alerta":
        base = mensajeModal('Notificación push', 'Ha llegado un nuevo menasje es tu bandeja', 'bi-mailbox-flag')


    return render(request, "app/mensajes.html", {'titulo':titulo, 'base': base, 'menu': generar_menu(request.user)})

def crud(request: HttpRequest):
    titulo = 'Implementación CRUD de una tabla en BD'
    return render(request, "app/crud.html", {'titulo':titulo,'menu': generar_menu(request.user)})

def busqueda(request: HttpRequest):
    titulo = 'Implementación de busqueda de registros con filtro (paginada)'
    return render(request, "app/busqueda.html", {'titulo':titulo,'menu': generar_menu(request.user)})

def detalle(request: HttpRequest):
    titulo = 'Implementación de un maestro detalle'
    return render(request, "app/detalle.html", {'titulo':titulo,'menu': generar_menu(request.user)})


def toastError(mensaje:str):
    return {'toast' : {
                  'titulo':'Error al procesar la solicitud',
                  'mensaje':mensaje,
                  'iconostyle':'bi bi-sign-stop text-danger fs-2  mx-2'
             }}

def toastOk(mensaje:str):
    return {'toast' : {
                  'titulo':'Solicitud procesada',
                  'mensaje':mensaje,
                  'iconostyle':'bi bi-check-circle-fill text-success fs-1 mx-2',
             }}

def mensajeModal(titulo:str, mensaje:str, icono:str):
    return {'modalMensaje' : {
                  'titulo':titulo,
                  'mensaje':mensaje,
                  'iconostyle':'bi ' + icono + ' text-success fs-1 mx-2',
             }}
