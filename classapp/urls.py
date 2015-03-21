from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'classapp/login.html'}),
    url(r'^', 'classapp.views.home_view'),
)
