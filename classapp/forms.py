from django import forms
from django.forms import ModelForm
from codathon2015.models import UVMUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ContactForm(ModelForm):
    class Meta:
        model = UVMUser
        fields = ['uvm_email',]
        widgets = {
                }