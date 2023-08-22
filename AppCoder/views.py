from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader
from .models import Curso, Profesor, Estudiante
from .forms import CursoForm

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

    return render(request,"AppCoder/inicio.html")

def profesores(request):
    profes = Profesor.objects.all()
    return render(request,"AppCoder/profesores.html", {"profes":profes})

def estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request,"AppCoder/estudiantes.html", {"estudiantes":estudiantes})

def cursos(request):
    cursos = Curso.objects.all()
    return render(request, "AppCoder/cursos.html", {"cursos":cursos})

def cursoFormulario(request):
    if request.method == "POST":
        mensaje = ""
        # nombre   = request.POST["nombre"]
        # comision = request.POST["comision"]
        # curso = Curso(nombre=str(nombre).capitalize(), comision=comision)
        # curso.save()

        form = CursoForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            nombre   = info["nombre"]
            comision = info["comision"]
            curso = Curso(nombre=str(nombre).capitalize(), comision=comision)
            curso.save()
            mensaje = "Curso creado satisfactoriamente!"
        else:
            mensaje = "Formulario inválido!"
        
        return render(request, "AppCoder/cursoFormulario.html", {"mensaje":mensaje})
    
    formulario_curso = CursoForm()
    return render(request, "AppCoder/cursoFormulario.html",{"formulario":formulario_curso})

def entregables(request):

    return render(request,"AppCoder/entregables.html")