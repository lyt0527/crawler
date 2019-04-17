from django.contrib import admin
# from django.urls import path
from django.conf.urls import url,include
from django.views.static import serve

# from crawler.settings import STATIC_ROOT

urlpatterns = [
    url('admin/', admin.site.urls),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    url(r'^account/',include('account.urls', namespace='account')),
    url(r'^function/',include('function.urls',namespace='function')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^export/', include('export.urls', namespace='export')),
    url(r'^receive/', include('receive.urls', namespace='receive')),

]