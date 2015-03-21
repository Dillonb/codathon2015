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

    def clean(self):
        cleaned_data = super(AddCourseForm, self).clean()
        crn_good = False
        subject_good = False
        number_good = False
        section_good = False

        if u'crn' in cleaned_data.keys():
            crn_good = not cleaned_data[u'crn'] is None
        if u'subject' in cleaned_data.keys():
            subject_good = not cleaned_data[u'subject'] is None
        if u'number' in cleaned_data.keys():
            number_good = not cleaned_data[u'number'] is None
        if u'section' in cleaned_data.keys():
            section_good = not cleaned_data[u'section'] is None

        if subject_good:
            cleaned_data[u'subject'] = cleaned_data[u'subject'].upper()

        if not (crn_good or (subject_good and section_good)):
            raise forms.ValidationError("Fill in either the CRN or the Subject/Section fields!")

        return cleaned_data


    term = forms.ChoiceField(choices=getTermChoices())
    # Either CRN
    crn = forms.IntegerField(required=False)
    # Or subject, number, section
    subject = forms.CharField(required=False)
    number = forms.IntegerField(required=False)
    section = forms.CharField(required=False)







class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    anon = forms.BooleanField(required=False,label="Post anonymously")

class NewReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    anon = forms.BooleanField(required=False,label="Post anonymously")
