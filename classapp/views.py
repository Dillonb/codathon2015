from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from classapp.models import *
from classapp.forms import *
import urllib, json

def home_view(request):
    """A view for / that redirects either to a login page, or to a list of courses the user is in."""
    if request.user.is_authenticated():
        return redirect("/courses/list/")
    else:
        return redirect("/accounts/login")

def logout_view(request):
    """A view for /accounts/logout that logs the user out."""
    logout(request)
    return redirect("/")

@login_required
def course_list_view(request):
    """A view to show a list of courses the user is in."""

    # Quick hack to disallow professors from logging in
    if hasattr(request.user,'ldap_user'): # If the current user is an ldap user (not a local user)
        # Loop through their affiliations
        for affiliation in request.user.ldap_user.attrs[u'edupersonaffiliation']:
            # If they're faculty, log them out and send them to the noprofessors page.
            if affiliation == u'Faculty':
                logout(request)
                return redirect("/noprofessors")

    # Grab the list of courses for this user, and render the template.
    courses = request.user.course_set.all()
    return render(request,"classapp/courselist.html",{"courses": courses})

@login_required
def course_add_view(request):
    """A view to allow the user to add a course to their profile."""
    form = AddCourseForm(data=request.POST)
    if form.is_valid(): # This form will only validate if we either have one of: (crn) or (subject, number, section) as well as term.
        url = ""
        using_crn = not form.cleaned_data['crn'] is None # If we have a crn, use it, otherwise use subject number section.

        # Two different urls to grab the same data.
        if using_crn:
            url = "https://www.uvm.edu/_api.d/v1/course-catalogue/term/" + str(form.cleaned_data['term']) + "/crn/" + str(form.cleaned_data['crn'])
        else:
            url = "https://www.uvm.edu/_api.d/v1/course-catalogue/term/" + str(form.cleaned_data['term']) + "/subject/" + str(form.cleaned_data['subject']) + "/course/" + str(form.cleaned_data['number'])

        # Grab and decode the json from the API
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        data = data[u'sections']

        # If we're not using a CRN, we were returned a list of sections. Loop through and find the right one.
        if not using_crn:
            for course in data:
                if course[u'section'] == form.cleaned_data['section']:
                    data = course
                    break # We found it, no need to keep looping.

        # Allow for multiple instructors.
        instructor_str = "N/A" # Default
        if len(data[u'instructors']) == 0:
            pass # Stick with default
        if len(data[u'instructors']) == 1:
            instructor_str = data[u'instructors'][0][u'first'] + " " + data[u'instructors'][0][u'last'] # Just one instructor.
        else: # Build a list of instructors.
            instructor_str = ""
            for instructor in data[u'instructors']:
                instructor_str += (instructor[u'first'] + " " + instructor[u'last'] + " ")

        # Grab our course - get it from the database, or create it if it doesn't exist (thanks Django)
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

        # If we had to create it, save it.
        if created:
            course.save() 
        request.user.course_set.add(course) # Assign our user to it.
        return redirect("/courses/list") # Bring the user back to the list of courses.

    else:
        # The form was invalid - meaning the user either didn't fill it out, or they filled it out with errors.
        return render(request,"classapp/addcourse.html", {"form": form})

@login_required
def course_view_view(request,courseid):
    """A view to view a course by id."""

    # We have two forms here, one to post to the course and one to reply to a post.
    post_form = NewPostForm(data=request.POST) # This form posts back to this page
    reply_form = NewReplyForm() # This one posts to a different page, don't try to grab data (it's meant for post_form if it exists)

    # Grab the course we're supposed to be viewing. 404 if it doesn't exist.
    course = get_object_or_404(Course, id=courseid)

    # If we have valid data for a post, make sure to save it BEFORE fetching data for the page, so we can see the new post immediately.
    if post_form.is_valid():
        post = Post(
                    user = request.user,
                    course = course,
                    content = post_form.cleaned_data['content'],
                    anon = post_form.cleaned_data['anon'],
                )
        post.save()

    # Grab all posts, ordered so most recent are first.
    posts = Post.objects.filter(course=course).order_by('-time')
    post_form = NewPostForm() # Clear the form, so old data doesn't stick in it when we display the page.
    return render(request, "classapp/courseview.html", {
        "course": course,
        "posts": posts,
        "new_post_form": post_form,
        "new_reply_form": reply_form
        })


@login_required
def post_reply_view(request, postid):
    """A view to save a reply to a post. Doesn't render anything, only redirects back to the course after either succeeding or failing."""
    # Grab our form and requested parent post
    form = NewReplyForm(data=request.POST)
    post = get_object_or_404(Post,id=postid)

    # If we have valid data, save our new comment.
    if form.is_valid():
        comment = Comment(
                user = request.user,
                post = post,
                content = form.cleaned_data['content'],
                anon = form.cleaned_data['anon'],
            )
        comment.save()
    # Return to the course page where we posted the reply.
    return redirect(post.course.get_absolute_url())


@login_required
def classmate_view(request,courseid):
    """A view to list all students in the class."""
    # Grab the course and all users in it, render the template.
    course = get_object_or_404(Course, id=courseid)
    users =  UVMUser.objects.filter(course=course).order_by("last_name")
    return render(request, "classapp/classmates.html",{"course": course, "users": users})

@login_required
def info_edit_view(request):
    """Returns a page that allows users to edit their information."""
    form = ContactForm(data=request.POST)

    # If we have valid data, update the current user object and save it.
    if form.is_valid():
        user = request.user
        user.facebook_url = form.cleaned_data['facebook_url']
        user.additional_email_1 = form.cleaned_data['additional_email_1']
        user.additional_email_2 = form.cleaned_data['additional_email_2']
        user.phone_number = form.cleaned_data['phone_number']

        user.save()
    # Render the same page again.
    return render(request,"classapp/info_form.html", {"form": form, "person":request.user})

def no_professors_view(request):
    """Renders a fun little "no professors allowed" page."""
    return render(request, "classapp/noprofessors.html")

@login_required
def course_leave_view(request, courseid):
    """A view to allow a user to leave a course. Only linked to, doesn't render anything, only redirects back."""
    course = get_object_or_404(Course, id=courseid)
    course.users.remove(request.user)
    return redirect("/courses/list")