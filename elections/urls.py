from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^ajax_get/$', views.ajax_get, name="ajax_get"),
    url(r'^ajax_post/$', views.ajax_post, name= "ajax_post"),
    url(r'^update_vote/$', views.update_vote, name='update_vote'),
    url(r'^get_last_modification/$', views.get_last_modification, name='get_last_modification'),
]