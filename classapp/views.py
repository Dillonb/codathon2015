from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from classapp.models import *
from classapp.forms import *
import urllib, json

def home_view(request):
    if request.user.is_authenticated():
        return redirect("/courses/list/")
    else:
        return redirect("/accounts/login")

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def course_list_view(request):
    if hasattr(request.user,'ldap_user'):
        print (request.user.ldap_user.attrs)
        for affiliation in request.user.ldap_user.attrs[u'edupersonaffiliation']:
            # If they're faculty, log them out and send them to the noprofessors page.
            if affiliation == u'Faculty':
                logout(request)
                return redirect("/noprofessors")
    print("You're allowed to access the site.")

    courses = request.user.course_set.all()
    return render(request,"classapp/courselist.html",{"courses": courses})

@login_required
def course_add_view(request):
    form = AddCourseForm(data=request.POST)
    if form.is_valid():
        print (form.cleaned_data)
        url = ""
        using_crn = not form.cleaned_data['crn'] is None
        if using_crn:
            url = "https://www.uvm.edu/_api.d/v1/course-catalogue/term/" + str(form.cleaned_data['term']) + "/crn/" + str(form.cleaned_data['crn'])
        else:
            url = "https://www.uvm.edu/_api.d/v1/course-catalogue/term/" + str(form.cleaned_data['term']) + "/subject/" + str(form.cleaned_data['subject']) + "/course/" + str(form.cleaned_data['number'])

        response = urllib.urlopen(url)
        data = json.loads(response.read())
        print(data)
        data = data[u'sections']
        if not using_crn:
            for course in data:
                if course[u'section'] == form.cleaned_data['section']:
                    data = course
                    break

        instructor_str = "None"
        if len(data[u'instructors']) == 0:
            pass
        if len(data[u'instructors']) == 1:
            instructor_str = data[u'instructors'][0][u'first'] + " " + data[u'instructors'][0][u'last']
        else:
            instructor_str = ""
            for instructor in data[u'instructors']:
                instructor_str += (instructor[u'first'] + " " + instructor[u'last'] + " ")

        course,created = Course.objects.get_or_create(
                term = data[u'term_code'],
                crn = data[u'crn'],
                subject = data[u'subject'],
                number = data[u'number'],
                instructor = instructor_str,
                section = data[u'section'],
                name = data[u'crse_title'],
                description = data[u'description']
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
    reply_form = NewReplyForm()

    course = get_object_or_404(Course, id=courseid)
    if post_form.is_valid():
        post = Post(
                    user = request.user,
                    course = course,
                    content = post_form.cleaned_data['content'],
                    anon = post_form.cleaned_data['anon'],
                )
        post.save()

    posts = Post.objects.filter(course=course).order_by('-time')
    post_form = NewPostForm()
    return render(request, "classapp/courseview.html", {
        "course": course,
        "posts": posts,
        "new_post_form": post_form,
        "new_reply_form": reply_form
        })


@login_required
def post_reply_view(request, postid):
    form = NewReplyForm(data=request.POST)
    if form.is_valid():
        post = get_object_or_404(Post,id=postid)

        comment = Comment(
                user = request.user,
                post = post,
                content = form.cleaned_data['content'],
                anon = form.cleaned_data['anon'],
            )
        print("Saving a comment")
        print(comment.user)
        comment.save()
        return redirect(post.course.get_absolute_url())
    else:
        print(request.POST)
        print(form.errors)
        return redirect(post.course.get_absolute_url())


@login_required
def classmate_view(request,courseid):
    course = get_object_or_404(Course, id=courseid)
    users =  UVMUser.objects.filter(course=course).order_by("last_name")
    return render(request, "classapp/classmates.html",{"course": course, "users": users})

@login_required
def info_edit_view(request):
    form = ContactForm(data=request.POST)

    if form.is_valid():
        print (form.cleaned_data)

        user = request.user
        user.facebook_url = form.cleaned_data['facebook_url']
        user.additional_email_1 = form.cleaned_data['additional_email_1']
        user.additional_email_2 = form.cleaned_data['additional_email_2']
        user.phone_number = form.cleaned_data['phone_number']

        user.save()
    return render(request,"classapp/info_form.html", {"form": form, "person":request.user})

def no_professors_view(request):
    return render(request, "classapp/noprofessors.html")

@login_required
def course_leave_view(request, courseid):
    course = get_object_or_404(Course, id=courseid)
    course.users.remove(request.user)
    return redirect("/courses/list")

# def profile_card_view(request):
# 	return render(request, "classapp/")
