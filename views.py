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

    if request.method == 'POST':
        for k, v in request.POST.items():
            print("%s: %s" % (k, v))

    matches = Match.objects.filter(matchday=m_nr)
    return render_to_response(
        'tippspiel/matchday_detail.html',
        {
            'number': m_nr,
            'matches': matches
        },
        context_instance=RequestContext(request)
    )


@login_required
def player_detail(request, player_name):
    p = get_object_or_404(Player, user__username=player_name)
    return render_to_response(
        'tippspiel/player_detail.html',
        {
            'player': p
        },
        context_instance=RequestContext(request)
    )
