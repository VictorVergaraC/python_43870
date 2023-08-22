from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader
from .models import Curso

# Create your views here.

def crear_curso(request):
    nombre_curso = "Programacion Basica"
    comision_curso = 98765
    print("Creando curso")
    curso = Curso(nombre=nombre_curso, comision=comision_curso)
    # curso.save()
    respuesta = f"Curso creado: {nombre_curso} - {comision_curso}"
    return HttpResponse(respuesta)

def listar_cursos(request):
    cursos = Curso.objects.all()
    respuesta = "<h2>Cursos</h2>"
    for curso in cursos:
        respuesta += f"Curso: {curso.nombre} - Comisión: {curso.comision}<br>"
    return HttpResponse(respuesta)

def inicio(request):

    return HttpResponse("Vista inicio")

def profesores(request):

    return HttpResponse("Vista profesores")

def estudiantes(request):

    return HttpResponse("Vista estudiantes")

def cursos(request):

    return HttpResponse("Vista cursos")

def entregables(request):

    return HttpResponse("Vista entregables")