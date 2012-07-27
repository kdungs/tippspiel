from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('tippspiel.views',
    url(r'^$', 'index_page'),

    url(r'^login/$', 'login_page'),
    url(r'^logout/$', 'logout_page'),

    url(r'^player/(?P<player_name>\w+)/$', 'player_page'),

    url(r'^matchdays/$', 'matchdays_page'),
    url(r'^matchday/(?P<matchday_number>\d+)/$', 'matchday_page'),
)