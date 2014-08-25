from django.conf.urls import patterns, url
from summer import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^list/', views.list, name='list'),
    url(r'^add_channel/', views.add_channel, name='add_channel'),
    url(r'^rijec/$', views.rijec, name='rijec'),  # JSON api
    url(r'^toplist/$', views.toplist, name='toplist'),
    url(r'^change_feed_status/$',
        views.change_feed_status,
        name='change_feed_status'),
)
