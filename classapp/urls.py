from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'classapp/home.html'}),
    url(r'^accounts/logout/$', 'classapp.views.logout_view'),
    url(r'^accounts/profile/$', 'classapp.views.course_list_view'),
    url(r'^accounts/edit/$', 'classapp.views.info_edit_view'),
    url(r'^courses/list/$', 'classapp.views.course_list_view'),
    url(r'^courses/add/$', 'classapp.views.course_add_view'),
    url(r'^courses/view/(?P<courseid>\d+)$', 'classapp.views.course_view_view'),
    url(r'^courses/leave/(?P<courseid>\d+)$', 'classapp.views.course_leave_view'),
    url(r'^postreply/(?P<postid>\d+)$', 'classapp.views.post_reply_view'),
    url(r'^courses/classmates/(?P<courseid>\d+)$', 'classapp.views.classmate_view'),
    url(r'^noprofessors/$', 'classapp.views.no_professors_view'),
    url(r'^$', 'classapp.views.home_view')
)
