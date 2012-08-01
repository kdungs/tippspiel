from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from tippspiel.models import Player, Team, Match, Tipp


@login_required
def matchday_detail(request, matchday_number):
    m_nr = int(matchday_number)
    if m_nr < 1 or m_nr > 34:
        raise Http404
    # build a range of 10 days that ideally has the current day in the center
    m_range = range(m_nr-4, m_nr+6)
    if m_range[0] < 1:
        m_range = [x-(m_range[0]-1) for x in m_range]
    elif m_range[-1] >= 35:
        m_range = [x-(m_range[-1]-34) for x in m_range]
    matches = Match.objects.filter(matchday=m_nr)
    return render_to_response(
        'tippspiel/matchday_detail.html',
        {
            'number': m_nr,
            'matchday_range': m_range,
            'matches': matches
        },
        context_instance=RequestContext(request)
    )


@login_required
def player_detail(request, player_name):
    from urllib import urlencode
    p = get_object_or_404(Player, user__username=player_name)
    return render_to_response(
        'tippspiel/player_detail.html',
        {
            'player': p,
            'gravatar': "http://gravatar.com/avatar/%s?s=120" % p.gravatar_hash()
        },
        context_instance=RequestContext(request)
    )
