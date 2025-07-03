# pokemon/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import PokemonRegistro

class ProfileEditForm(UserChangeForm):
    # Eliminamos el campo de contraseña del formulario
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

# Formulario para ingresar detalles de captura del Pokémon
class PokemonCapturaForm(forms.ModelForm):
    class Meta:
        model = PokemonRegistro
        fields = ['nivel', 'naturaleza', 'shiny', 'genero', 'comentarios']
        labels = {
            'nivel': 'Nivel',
            'naturaleza': 'Naturaleza',
            'shiny': '¿Es shiny?',
            'genero': 'Género',
            'comentarios': 'Comentarios adicionales'
        }
        widgets = {
            'nivel': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'naturaleza': forms.TextInput(attrs={'class': 'form-control'}),
            'shiny': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
