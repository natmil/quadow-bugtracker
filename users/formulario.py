from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil


# Clase para el formulario de registro
class FormularioRegistro(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User  # Guardaremos los usuarios en el modelo User de Django
        # Mostraremos en el formulario los siguientes campos en tal orden
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


# Clase para el formulario de actualización del usuario
class FormularioActualizarUsuario(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


# Clase para el formulario de actualizar el perfil del usuario
class FormularioActualizarPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen']
