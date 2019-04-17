from django.conf.urls import url
from . import views
app_name = 'receive'

urlpatterns = [
    url(r'^receive_all/$', views.receive_content, name='receive_content')
]