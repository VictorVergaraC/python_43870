from django import forms

class CursoForm(forms.Form):
    nombre   = forms.CharField(max_length=50) # Es un campo de strings
    comision = forms.IntegerField()
    