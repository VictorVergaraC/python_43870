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
    