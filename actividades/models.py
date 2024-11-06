from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.

class Usuario(AbstractUser):
    facultad = models.ForeignKey('Facultad', on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='usuario_custom_set', blank=True) 
    user_permissions = models.ManyToManyField(Permission, related_name='usuario_custom_set', blank=True)
    
    def __str__(self):
        return self.username
 

class TipoActividad(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self): 
        return self.nombre


class NombreActividad(models.Model):
    tipo = models.ForeignKey(TipoActividad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  
    
    def __str__(self): 
        return f"{self.tipo.nombre} - {self.nombre}"

    
class Actividad(models.Model): 
    nombre = models.ForeignKey(NombreActividad, on_delete=models.CASCADE, null=True, blank=True) 
    descripcion = models.TextField() 
    fecha_inicio = models.DateField() 
    fecha_fin = models.DateField() 
    horario_inicio = models.TimeField() 
    horario_fin = models.TimeField() 
    resultado = models.CharField(max_length=100) 
    puntos_facultad = models.IntegerField() 
    estado = models.CharField(max_length=50) 
    tipo = models.ForeignKey(TipoActividad, on_delete=models.CASCADE)
     
    def __str__(self): 
        return self.nombre 
    
class Asistencia(models.Model): 
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) 
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE) 
    asistencia = models.BooleanField() 
    
    def __str__(self): 
        return f"{self.usuario} - {self.actividad}" 
    
class Notificacion(models.Model): 
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) 
    mensaje = models.TextField() 
    fecha = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self): 
        return f"Notificación para {self.usuario}" 
    
class Facultad(models.Model): 
    nombre = models.CharField(max_length=100) 
    puntos_totales = models.IntegerField() 
    
    def __str__(self): 
        return self.nombre 
    
class Resultado(models.Model): 
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE) 
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='resultados') 
    puntos = models.IntegerField()
    
    def __str__(self): 
        return f"{self.facultad} - {self.actividad}"
