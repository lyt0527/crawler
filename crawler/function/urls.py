from  django.conf.urls import url
from . import views
app_name = 'function'

urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^navigator/$',views.navigator,name='navigator'),
    url(r'^count/$',views.count,name='count'),
    url(r'^count_day/$',views.count_day,name='count_day'),
    url(r'^count1/$',views.count1,name='count1'),
    url(r'^comment/$',views.comment,name='comment'),
    url(r'^judgement/$',views.judgement,name='judgement'),
    url(r'^train/$',views.train,name='train'),
    url(r'^rejudge/$', views.rejudge, name='rejudge'),
    url(r'^message/$', views.message, name='message'),
    url(r'^all_page/$', views.all_page, name='all_page'),
    # url(r'^comment_list/$',views.comment_list,name='comment_list'),
    url(r'^comment_content/$',views.comment_content,name='comment_content'),
    url(r'^submit_newscore/$',views.submit_newscore,name='submit_newScore'),
    url(r'^changeitems/$',views.changeitems,name='changeitems'),
    url(r'^admin/$',views.admin,name='admin'),
    url(r'^save_train/$', views.save_train, name='save_train'),
    url(r'^precision/$', views.precision, name='precision'),
    url(r'^last_rejudge/$', views.last_rejudge, name='last_rejudge'),
    url(r'^reply/$',views.reply, name='reply'),
    url(r'^show_reply/$',views.show_reply, name='show_reply'),
    url(r'^plotting/$',views.plotting, name='plotting'),
    url(r'^news/$',views.news, name='news'),
    # url(r'^export_excel/$',views.export_excel, name='export_excel'),
    url(r'^is_ignore/$',views.is_ignore, name='is_ignore'),
    # url(r'^download_excel/$',views.download_excel, name='download_excel'),
]