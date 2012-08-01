from django.conf.urls import patterns, url
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView

from tippspiel.models import Player, Team, Match, Tipp


urlpatterns = patterns('django.contrib.auth',
    url(r'^login/$', 'views.login', {'template_name': 'tippspiel/login.html'}),
    url(r'^logout/$', 'views.logout_then_login'),
)

urlpatterns += patterns('tippspiel.views',
    url(
        r'^$',
        login_required(TemplateView.as_view(template_name='tippspiel/overview.html')),
        name="tippspiel_overview"
    ),

    url(
        r'^matchdays/$',
        login_required(ListView.as_view(
            queryset=range(1, 35),
            context_object_name='matchdays',
            template_name='tippspiel/matchday_list.html'
        )),
        name="tippspiel_matchday_list"
    ),

    url(
        r'^matchday/(?P<matchday_number>\d+)/$',
        'matchday_detail',
        name="tippspiel_matchday_detail"
    ),

    url(
        r'^matches/$',
        login_required(ListView.as_view(
            queryset=Match.objects.order_by('date'),
            context_object_name='matches'
        )),
        name='tippspiel_match_list'
    ),

    url(
        r'^match/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            model=Match
        )),
        name="tippspiel_match_detail"
    ),

    url(
        r'^ranking/$',
        login_required(ListView.as_view(
            queryset=Player.objects.order_by('rank'),
            context_object_name='players',
            template_name='tippspiel/player_list.html'
        )),
        name="tippspiel_player_list"
    ),

    url(
        r'^player/(?P<player_name>\w+)/$',
        'player_detail',
        name="tippspiel_player_detail"
    )
)