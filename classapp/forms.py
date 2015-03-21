from django import forms
from django.forms import ModelForm
from classapp.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import urllib
import json

class ContactForm(ModelForm):
    
    facebook_url = forms.CharField(required=False)
    additional_email_1 = forms.CharField(required=False)
    additional_email_2 = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    
    class Meta:
        model = UVMUser
        fields = ['facebook_url', 'additional_email_1','additional_email_2','phone_number']

class AddCourseForm(forms.Form):
    def getTermChoices(): # Because of how this is called below, don't add a self argument..

        url = "https://www.uvm.edu/_api.d/v1/course-catalogue/terms"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        choices = ()
        for term in data[u'terms']:
            choices += ( (term[u'code'], term[u'name']), )

        return choices


    term = forms.ChoiceField(choices=getTermChoices())
    crn = forms.IntegerField()



class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class NewReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
