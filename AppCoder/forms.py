from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CursoForm(forms.Form):
    nombre   = forms.CharField(max_length=50) # Es un campo de strings
    comision = forms.IntegerField()
    
class ProfesorForm(forms.Form):
    nombre    = forms.CharField(max_length=50)
    apellido  = forms.CharField(max_length=50)
    email     = forms.EmailField()
    profesion = forms.CharField(max_length=50)

class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre")
    last_name  = forms.CharField(label="Apellido")
    email      = forms.EmailField(label="Email")
    password1  = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2  = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    class Meta:
        model=User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        help_texts = {campo:"" for campo in fields} # para cada uno de los campos del formulario, le asigna un valor vacio

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"].capitalize()
        user.last_name = self.cleaned_data["last_name"].capitalize()
        if commit:
            user.save()
        return user
    
# PRE ENTREGA

class ProductosForm(forms.Form):
    descripcion = forms.CharField(max_length=50)
    marca       = forms.CharField(max_length=50)
    precio      = forms.IntegerField()
    stock       = forms.IntegerField()