from django.shortcuts import render_to_response, get_object_or_404
from tippspiel.models import Player, Team, Match, Tipp
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext

@login_required
def index_page(request):
    return render_to_response(
        'tippspiel/index.html',
        context_instance=RequestContext(request)
    )


def login_page(request):
    return render_to_response('tippspiel/login.html')


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def ranking_page(request):
    players = Player.objects.order_by('rank')
    return render_to_response(
        'tippspiel/ranking.html',
        {
            'players': players
        },
        context_instance=RequestContext(request)
    )


@login_required
def player_page(request, player_name):
    from urllib import urlencode
    p = get_object_or_404(Player, user__username=player_name)
    return render_to_response(
        'tippspiel/player.html',
        {
            'player': p,
            'gravatar': "http://gravatar.com/avatar/%s?s=120" % p.gravatar_hash()
        },
        context_instance=RequestContext(request)
    )


@login_required
def matchdays_page(request):
    return render_to_response(
        'tippspiel/matchdays.html',
        {
            'matchdays': range(1, 35)
        },
        context_instance=RequestContext(request)
    )


@login_required
def matchday_page(request, matchday_number):
    m_nr = int(matchday_number)
    # build a range of 10 days that ideally has the current day in the center
    m_range = range(m_nr-4, m_nr+6)
    if m_range[0] < 1:
        m_range = [x-(m_range[0]-1) for x in m_range]
    elif m_range[-1] >= 35:
        m_range = [x-(m_range[-1]-34) for x in m_range]
    matches = Match.objects.filter(matchday=m_nr)
    return render_to_response(
        'tippspiel/matchday.html',
        {
            'number': m_nr,
            'matchday_range': m_range,
            'matches': matches
        },
        context_instance=RequestContext(request)
    )
