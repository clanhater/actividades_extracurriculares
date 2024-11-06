from django.contrib import admin
from .models import Usuario, Actividad, Asistencia, Notificacion, Facultad, Resultado, TipoActividad, NombreActividad
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ('username', 'email', 'facultad', 'is_staff', 'is_active')  
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('facultad',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'facultad', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(TipoActividad) 
class TipoActividadAdmin(admin.ModelAdmin): 
    list_display = ('nombre',) 
    
@admin.register(NombreActividad) 
class NombreActividadAdmin(admin.ModelAdmin): 
    list_display = ('tipo', 'nombre')


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'tipo')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('estado', 'tipo')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'actividad', 'asistencia')
    search_fields = ('usuario__nombre', 'actividad__nombre')
    list_filter = ('asistencia',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje', 'fecha')
    search_fields = ('usuario__nombre', 'mensaje')
    list_filter = ('fecha',)

@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntos_totales')
    search_fields = ('nombre',)

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('facultad', 'actividad', 'puntos',)
    search_fields = ('facultad__nombre', 'actividad__nombre')
    list_filter = ('actividad',)




