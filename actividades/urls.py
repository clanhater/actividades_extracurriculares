from django.urls import path
from .views import *
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("actividades/", ActividadListView.as_view(), name="actividad_list"),
    path("actividad/nueva/", ActividadCreateView.as_view(), name="actividad_create"),
    path(
        "actividad/editar/<int:pk>/",
        ActividadUpdateView.as_view(),
        name="actividad_update",
    ),
    path(
        "actividad/eliminar/<int:pk>/",
        ActividadDeleteView.as_view(),
        name="actividad_delete",
    ),
    path(
        "actividad/<int:actividad_id>/participantes/",
        registrar_participantes,
        name="registrar_participantes",
    ),
    path("horarios/", publicar_horarios, name="publicar_horarios"),
    path('perfil/', perfil, name='perfil'),
    path(
        "actividad/<int:actividad_id>/asistencia/",
        registrar_asistencia,
        name="registrar_asistencia",
    ),
    path(
        "actividad/<int:actividad_id>/lista_asistencia/",
        lista_asistencia,
        name="lista_asistencia",
    ),
    path(
        "actividad/<int:actividad_id>/resultado/",
        registrar_resultado,
        name="registrar_resultado",
    ),
    path("informe_final/", generar_informe_final, name="generar_informe_final"),
    path("informe_diario/", generar_informe_diario, name="generar_informe_diario"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
