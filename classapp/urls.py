from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'classapp/home.html'}),
    url(r'^accounts/logout/$', 'classapp.views.logout_view'),
    url(r'^accounts/profile/$', 'classapp.views.course_list_view'),
    url(r'^courses/list/$', 'classapp.views.course_list_view'),
    url(r'^courses/add/$', 'classapp.views.course_add_view'),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'classapp/home.html'}),
)
