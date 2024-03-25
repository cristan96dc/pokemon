from django.db import models

# Create your models here.

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=20)

class Licencia(models.Model):
    nombre = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    
class Registro(models.Model):
    nombre_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    numero_usuario = models.IntegerField()
    numero_licencia = models.ForeignKey(Licencia, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    fecha_presentacion = models.DateField()
    def _str_(self):
        return f"ID: {self.id} - Usuario: {self.nombre_usuario.nombre} - Número de Usuario: {self.numero_usuario} - Número de Licencia: {self.numero_licencia.numero}"
    



