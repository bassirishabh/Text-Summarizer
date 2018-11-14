from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from django.contrib.auth.views import login,logout

urlpatterns=[
    # /Summarizer/
    url(r'^$',views.home,name='home'),
    url(r'^form/$',views.form,name='form'),
    url(r'^login/$',views.LoginUserform.as_view(),name='login'),
    url(r'^logout/$',views.logoutt,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^error/$',TemplateView.as_view(template_name="Summarizer/error.html"),name='v'),

    url(r'^download/(?P<file>.*)/$', views.download, name='download1'),
    url(r'^download1/(?P<id>.*)/$', views.download1, name='download2'),
    url(r'^url/$',views.url,name='url'),
    url(r'^demo/$',views.demo,name='demo'),
    url(r'^detail/$',views.detail,name='detail'),
    url(r'^sendmessage/$',views.messagesend,name='send'),
    url(r'^check/$',views.check,name='check'),


]
