from django.contrib import admin
from .models import Curso, Estudiante, Profesor, Entregable, Producto, Vendedor, Categoria, Avatar

# Register your models here.

admin.site.register(Curso)
admin.site.register(Estudiante)
admin.site.register(Profesor)
admin.site.register(Entregable)
admin.site.register(Producto)
admin.site.register(Vendedor)
admin.site.register(Categoria)
admin.site.register(Avatar)