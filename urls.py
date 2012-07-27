from django.conf.urls import patterns, url

urlpatterns = patterns('tippspiel.views',
    url(r'^$', 'index'),
    url(r'^player/(?P<player_name>\w+)$', 'player'),
)