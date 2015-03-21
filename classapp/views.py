from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from classapp.models import *
from classapp.forms import *
import urllib, json

def home_view(request):
    if request.user.is_authenticated():
        return redirect("/courses/list")
    else:
        return render(request, "classapp/home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

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
                name = data[u'crse_title'],
                )
        course.save()
        request.user.course_set.add(course)
        print(data)
        return redirect("/courses/list")

    else:
        return render(request,"classapp/addcourse.html", {"form": form})

@login_required
def course_view_view(request,courseid):
    post_form = NewPostForm(data=request.POST)
    course = get_object_or_404(Course, id=courseid)
    if post_form.is_valid():
        post = Post(
                    user = request.user,
                    course = course,
                    content = post_form.cleaned_data['content']
                )
        post.save()

    posts = Post.objects.filter(course=course).order_by('-time')
    post_form = NewPostForm()
    return render(request, "classapp/courseview.html", {"course": course, "posts": posts, "new_post_form": post_form })


@login_required
def classmate_view(request,courseid):
    course = get_object_or_404(Course, id=courseid)
    users =  UVMUser.objects.filter(course=course)
    return render(request, "classapp/classmates.html",{"course": course, "users": users})

@login_required
def info_edit_view(request):
    form = ContactForm(data=request.POST)

    if form.is_valid():
        pass
    else:
        return render(request,"classapp/info_form.html", {"form": form, "person":request.user})
# def profile_card_view(request):
# 	return render(request, "classapp/")
