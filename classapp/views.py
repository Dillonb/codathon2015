from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from classapp.models import *
from classapp.forms import *
import urllib, json

def home_view(request):
	return render(request, "classapp/home.html")

def logout_view(request):
    logout(request)
    return render(request, "classapp/loggedout.html")

@login_required
def course_list_view(request):
    courses = request.user.course_set.all()
    return render(request,"classapp/courselist.html",{"courses": courses})

@login_required
def course_add_view(request):
    form = AddCourseForm(data=request.POST)

    if form.is_valid():
        url = "https://www.uvm.edu/_api.d/v1/course-catalogue/term/" + str(form.cleaned_data['term']) + "/crn/" + str(form.cleaned_data['crn'])
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        print(data)
        data = data[u'sections']
        instructor_str = "None"
        if len(data[u'instructors']) == 0:
            pass # Leave default value of None
        if len(data[u'instructors']) == 1:
            instructor_str = data[u'instructors'][0][u'first'] + " " + data[u'instructors'][0][u'last']
        else:
            instructor_str = ""
            for instructor in data.instructors:
                instructor_str += (instructor.first + " " + instructor.last)

        course,created = Course.objects.get_or_create(
                term = data[u'term_code'],
                crn = data[u'crn'],
                subject = data[u'subject'],
                number = data[u'number'],
                instructor = instructor_str,
                section = data[u'section'],
                )
        course.save()
        request.user.course_set.add(course)
        print(data)
        return redirect("/courses/list")

    else:
        return render(request,"classapp/addcourse.html", {"form": form})

@login_required
def info_edit_view(request):
    form = ContactForm(request)

    if form.is_valid():
        pass
    else:
        return render(request,"classapp/edit_info.html")
# def profile_card_view(request):
# 	return render(request, "classapp/")
