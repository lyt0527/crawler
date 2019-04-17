from django.conf.urls import url
from django.contrib.auth import views as auth_views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from .views import *

app_name = 'account'

urlpatterns = [
    url(r'^login/$',auth_views.LoginView.as_view(template_name="account/login.html"),name='auth_login'),
    # url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', auth_logout, name='logout'),
    url(r'^api/v1/login/$', obtain_jwt_token, name='login'),
]