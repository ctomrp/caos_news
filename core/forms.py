from django import forms 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group,User
from .models import NewsCategory,NewsState

class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=2,max_length=15)
    name = forms.CharField(min_length=3,max_length=15)
    last_name = forms.CharField(min_length=5,max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    email2 = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        email2 = cleaned_data.get('email2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden!')
        if email and email2 and email != email2:
            raise forms.ValidationError('Los correos no coinciden!')
        
# @receiver(post_save,sender=User)
# def assign_default_group(sender,instance,created,**kwargs):
#      if created:
#         group = Group.objects.get(name='Lector')
#         instance.groups.add(group) 

class crearNoticiaForm(forms.Form):
    title = forms.CharField(max_length=100)
    article = forms.CharField(max_length=150)
    category = forms.ModelChoiceField(queryset=NewsCategory.objects.all())
    photo = forms.ImageField()
    ubicacion = forms.CharField(max_length=40)

