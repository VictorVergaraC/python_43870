from django.db import models

# Create your models here.

class Curso(models.Model):
    nombre   = models.CharField(max_length=50) # Es un campo de strings
    comision = models.IntegerField()

    def __str__(self):
        salida = self.nombre +" - "+ str(self.comision)
        return str(salida)


class Estudiante(models.Model):
    nombre   = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email    = models.EmailField()

    def __str__(self):
        salida = self.nombre +" "+ str(self.apellido)
        return str(salida)
    

class Profesor(models.Model):
    nombre    = models.CharField(max_length=50)
    apellido  = models.CharField(max_length=50)
    email     = models.EmailField()
    profesion = models.CharField(max_length=50)

    def __str__(self):
        salida = self.nombre +" "+ str(self.apellido)
        return str(salida)
    

class Entregable(models.Model):
    nombre        = models.CharField(max_length=50)
    fecha_entrega = models.DateField()
    entregado     = models.BooleanField()

# PRE ENTREGA 3

class Producto(models.Model):
    descripcion = models.CharField(max_length=50)
    marca       = models.CharField(max_length=50)
    precio      = models.IntegerField()
    stock       = models.IntegerField()

    def __str__(self): # no me funcionaba con: return f" ... "
        return f"{self.descripcion} ({self.marca})"

class Vendedor(models.Model):
    nombre    = models.CharField(max_length=50)
    apellido  = models.CharField(max_length=50)
    email     = models.EmailField()
    direccion = models.CharField(max_length=50)
    seccion   = models.CharField(max_length=50)

    def __str__(self):
        salida = self.nombre +" "+ str(self.apellido)
        return str(salida)
    
class Categoria(models.Model):
    nombre      = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    activo      = models.BooleanField()

    def __str__(self):
        return str(self.nombre)