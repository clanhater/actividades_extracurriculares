from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import Actividad, Usuario

######### RF1 #########
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=100)

######### RF2 RF3 RF4 RF5 ###########
class ActividadForm(forms.ModelForm): 
    class Meta: 
        model = Actividad 
        fields = '__all__'
        
    def clean(self): 
        cleaned_data = super().clean() 
        if cleaned_data['fecha_fin'] < cleaned_data['fecha_inicio']: 
            self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a la fecha de inicio.') 
        return cleaned_data
    

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Usuario
        fields = ('username', 'email', 'facultad')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'facultad')
