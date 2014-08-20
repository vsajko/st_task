from django.conf.urls import patterns, url
from summer import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^list/', views.list, name='list'),
    url(r'^add_channel/', views.add_channel, name='add_channel'),

)
