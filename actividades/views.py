from datetime import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import ActividadForm, LoginForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Actividad, Asistencia, Facultad, Notificacion, Resultado, Usuario
from . import models
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def index(request): 
    actividades_destacadas = Actividad.objects.all()[:2]
    num = range(1, 11) 
    return render(request, 'actividades/index.html', { 'actividades_destacadas': actividades_destacadas, 'num': num, })

############ RF1 ##############
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = LoginForm()
    return render(request, "actividades/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def admin_actividad_view(request):
    actividades = Actividad.objects.all()
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_actividad')
    else:
        form = ActividadForm()
    return render(request, 'actividades/admin_actividad.html', {'actividades': actividades, 'form': form})



######### RF2 RF3 RF4 RF5 ###########
class ActividadListView(ListView):
    model = Actividad
    template_name = "actividades/actividad_list.html"
    paginate_by = 10
    
    def get_queryset(self): 
        queryset = super().get_queryset() 
        nombre = self.request.GET.get('nombre') 
        if nombre: 
            queryset = queryset.filter(nombre__icontains=nombre) 
        return queryset


class ActividadCreateView(CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = "actividades/actividad_form.html"
    success_url = reverse_lazy("actividad_list")


class ActividadUpdateView(UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = "actividades/actividad_form.html"
    success_url = reverse_lazy("actividad_list")


class ActividadDeleteView(DeleteView):
    model = Actividad
    template_name = "actividades/actividad_confirm_delete.html"
    success_url = reverse_lazy("actividad_list")


######### RF6 ###########
def registrar_participantes(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    if request.method == "POST":
        usuarios = request.POST.getlist("usuarios")
        for usuario_id in usuarios:
            usuario = Usuario.objects.get(id=usuario_id)
            Asistencia.objects.create(
                usuario=usuario, actividad=actividad, asistencia=True
            )
        return redirect("actividad_list")
    usuarios = Usuario.objects.all()
    return render(
        request,
        "registrar_participantes.html",
        {"actividad": actividad, "usuarios": usuarios},
    )


######### RF7 RF8 RF9 ###########
def publicar_horarios(request):
    actividades = Actividad.objects.all()
    return render(request, "actividades/horarios.html", {"actividades": actividades})


def notificar_asignacion(usuario, actividad):
    mensaje = f"Has sido asignado a la actividad {actividad.nombre} el {actividad.fecha_inicio}."
    Notificacion.objects.create(usuario=usuario, mensaje=mensaje)


def notificar_cambio_horario(actividad):
    usuarios = Asistencia.objects.filter(actividad=actividad).values_list(
        "usuario", flat=True
    )
    for usuario_id in usuarios:
        usuario = Usuario.objects.get(id=usuario_id)
        mensaje = f"El horario de la actividad {actividad.nombre} ha cambiado a {actividad.fecha_inicio} {actividad.horario_inicio}."
        Notificacion.objects.create(usuario=usuario, mensaje=mensaje)


######### RF10 RF11 RF12 ###########
@login_required
def perfil(request):
    user = request.user
    if user.is_staff:
        actividades_por_tipo = {}
        actividades = Actividad.objects.all().order_by('tipo')
        for actividad in actividades:
            if actividad.tipo not in actividades_por_tipo:
                actividades_por_tipo[actividad.tipo] = []
            actividades_por_tipo[actividad.tipo].append(actividad)
    else:
        actividades_participadas = user.actividades.filter(fecha__lt=timezone.now()).order_by('fecha')
        proximas_actividades = user.actividades.filter(fecha__gt=timezone.now()).order_by('fecha')
    return render(request, 'actividades/perfil.html', {
        'user': user,
        'actividades_por_tipo': actividades_por_tipo if user.is_staff else [],
        'actividades_participadas': actividades_participadas if not user.is_staff else [],
        'proximas_actividades': proximas_actividades if not user.is_staff else [],
    })



######### RF13 RF14 ###########
def registrar_asistencia(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    if request.method == "POST":
        asistencias = request.POST.getlist("asistencia")
        for asistencia_id in asistencias:
            asistencia = Asistencia.objects.get(id=asistencia_id)
            asistencia.asistencia = True
            asistencia.save()
        return redirect("actividad_list")
    usuarios = Usuario.objects.all()
    return render(
        request,
        "actividades/registrar_asistencia.html",
        {"actividad": actividad, "usuarios": usuarios},
    )


def lista_asistencia(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    asistencias = Asistencia.objects.filter(actividad=actividad)
    return render(
        request,
        "actividades/lista_asistencia.html",
        {"actividad": actividad, "asistencias": asistencias},
    )


######### RF15 RF16 RF17 RF18 ###########
def registrar_resultado(request, actividad_id): 
    actividad = get_object_or_404(Actividad, id=actividad_id) 
    if request.method == 'POST': 
        resultados = request.POST.getlist('resultados') 
        for resultado in resultados: 
            facultad_id, puntos, posicion = resultado.split(',') 
            facultad = Facultad.objects.get(id=facultad_id) 
            Resultado.objects.create(actividad=actividad, facultad=facultad, puntos=puntos, posicion=posicion) 
        return redirect('actividad_list') 
    facultades = Facultad.objects.all() 
    return render(request, 'actividades/registrar_resultado.html', {'actividad': actividad, 'facultades': facultades}) 

def calcular_ganador(): 
    actividades = Actividad.objects.all() 
    facultad_ganadora = None 
    max_puntos = 0 
    for facultad in Facultad.objects.all(): 
        puntos_totales = Resultado.objects.filter(facultad=facultad).aggregate(models.Sum('puntos'))['puntos__sum'] 
        if puntos_totales > max_puntos: 
            max_puntos = puntos_totales 
            facultad_ganadora = facultad 
    return facultad_ganadora


######### RF19 RF20 ###########
def generar_informe_final(request):
    resultados = Resultado.objects.all()
    return render(request, 'actividades/informe_final.html', {'resultados': resultados})

def generar_informe_diario(request):
    asistencias = Asistencia.objects.filter(actividad__tipo__in=['Guardia Estudiantil', 'TSU'], actividad__fecha_inicio=timezone.now().date())
    return render(request, 'actividades/informe_diario.html', {'asistencias': asistencias})