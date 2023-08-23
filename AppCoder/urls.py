from django.urls import path
from .views import *

urlpatterns = [
    path('crear_curso', crear_curso),
    path('listar_cursos', listar_cursos),
    path('profesores', profesores, name="profesores"),
    path('estudiantes', estudiantes, name="estudiantes"),
    path('cursos', cursos, name="cursos"),
    path('entregables', entregables, name="entregables"),
    path('busquedaComision', busquedaComision, name="busquedaComision"),
    path('buscar', buscar, name="buscar"),
    path('eliminarProfesor/<id>', eliminarProfesor, name="eliminarProfesor"),
    path('editarProfesor/<id>', editarProfesor, name="editarProfesor"),
]