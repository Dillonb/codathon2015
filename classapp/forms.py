from django import forms
from django.forms import ModelForm
from classapp.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ContactForm(ModelForm):
    class Meta:
        model = UVMUser
        fields = ['facebook_url','additional_email_1', 'additional_email_2', 'phone_number']
        widgets = {
                }

class AddCourseForm(forms.Form):
    term = forms.CharField()
    crn = forms.IntegerField()

class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class NewReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
