from django.urls import path
from .views import *

urlpatterns = [
    path('crear_curso', crear_curso),
    path('listar_cursos', listar_cursos),
    path('profesores', profesores),
    path('estudiantes', estudiantes),
    path('cursos', cursos),
    path('entregables', entregables),
]