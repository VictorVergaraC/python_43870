from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader
from .models import Curso, Profesor, Estudiante
from .forms import CursoForm, ProfesorForm

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

    formulario = ProfesorForm()
    mensaje = ""
    if request.method == "POST":

        form = ProfesorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            nombre    = data["nombre"]
            apellido  = data["apellido"]
            email     = data["email"]
            profesion = data["profesion"]

            new_profe = Profesor(nombre=str(nombre).capitalize(), apellido=str(apellido).capitalize(), email=str(email).lower(), profesion = str(profesion).capitalize())
            new_profe.save()
            mensaje = "Profesor creado!"
        else:
            mensaje = "Formulario inválido!"
            pass

    return render(request,
                  "AppCoder/profesores.html", 
                  {"profes":profes, "formulario":formulario, "mensaje":mensaje}
            )

def estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request,
                  "AppCoder/estudiantes.html", 
                  {"estudiantes":estudiantes}
            )



def cursos(request):
    if request.method == "POST":
        # nombre   = request.POST["nombre"]
        # comision = request.POST["comision"]
        # curso = Curso(nombre=str(nombre).capitalize(), comision=comision)
        # curso.save()
        mensaje = "Formulario inválido!"
        form = CursoForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            nombre   = info["nombre"]
            comision = info["comision"]
            curso = Curso(nombre=str(nombre).capitalize(), comision=comision)
            curso.save()
            mensaje = "Curso creado satisfactoriamente!"
            
        return render(request, "AppCoder/cursos.html", {"mensaje":mensaje})
    
    formulario_curso = CursoForm()
    return render(request, "AppCoder/cursos.html",{"formulario":formulario_curso})

def entregables(request):

    return render(request,"AppCoder/cursos.html")

def busquedaComision(request):

    return render(request,"AppCoder/busquedaComision.html")

def buscar(request):
    comision = request.GET["comision"]
    mensaje = "Sin resultados!"
    if comision != "":
        listar_cursos = Curso.objects.filter(comision__icontains=comision)
        if listar_cursos:
            mensaje = ""
    return render(
            request,
            "AppCoder/resultadosBusqueda.html",
            {"cursos":listar_cursos, "mensaje":mensaje}
        )