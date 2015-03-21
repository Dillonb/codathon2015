from django import forms
from django.forms import ModelForm
from classapp.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ContactForm(ModelForm):
    class Meta:
        model = UVMUser
        fields = ['uvm_email',]
        widgets = {
                }

class AddCourseForm(forms.Form):
    crn = forms.IntegerField()
