from django.conf.urls import url
from . import views
app_name = 'receive'

urlpatterns = [
    url(r'^export_all/$', views.export_content, name='export_content')
]