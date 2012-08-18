# coding=utf-8

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from tippspiel.models import Player, Team, Match, Tipp

import re


@login_required
def overview(request):
    player = get_object_or_404(Player, user=request.user)
    top_players = Player.objects.order_by('-score', 'user__username')[:3]
    upcoming_matchday = Match.objects.filter(date__gt=timezone.now()).order_by('date')[0].matchday
    upcoming_matchdays = filter(lambda x: x<35, [upcoming_matchday+i for i in (0, 1, 2)])
    return render_to_response(
        'tippspiel/overview.html',
        {
            'player': player,
            'top_players': top_players,
            'upcoming_matchdays': upcoming_matchdays
        },
        context_instance=RequestContext(request)
    )


@login_required
@csrf_protect
def matchday_detail(request, matchday_number):
    m_nr = int(matchday_number)
    if m_nr < 1 or m_nr > 34:
        # testing
        if m_nr != 0:
            raise Http404

    if request.method == 'POST':
        for k, v in request.POST.items():
            if k.startswith('Tipp-'):
                try:
                    match_id = int(k.strip('Tipp-'))
                except:
                    raise Http404
                m = re.match(r'^(?P<score_home>\d+):(?P<score_visitor>\d+)$', v)
                if m:
                    match = get_object_or_404(Match, pk=match_id)
                    if not match.has_started():
                        try:
                            tipp = Tipp.objects.get(player__user=request.user, match__id=match_id)
                        except:
                            tipp = None
                        score_home = m.group('score_home')
                        score_visitor = m.group('score_visitor')
                        if tipp:
                            tipp.date = timezone.now()
                            tipp.score_home = score_home
                            tipp.score_visitor = score_visitor
                        else:
                            tipp = Tipp(
                                player=Player.objects.get(pk=request.user.pk),
                                match=match,
                                date=timezone.now(),
                                score_home=score_home,
                                score_visitor=score_visitor
                            )
                        tipp.save()
        return HttpResponseRedirect(reverse("tippspiel_matchday_detail", kwargs={'matchday_number':m_nr}))

    matches = Match.objects.filter(matchday=m_nr)
    tipps = Tipp.objects.filter(player__user=request.user).filter(match__matchday=m_nr)
    tipps_by_matches = {t.match.pk: t for t in tipps}

    return render_to_response(
        'tippspiel/matchday_detail.html',
        {
            'number': m_nr,
            'matches': matches,
            'tipps': tipps_by_matches
        },
        context_instance=RequestContext(request)
    )


@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    tipps = None
    if match.has_started():
        tipps = Tipp.objects.filter(match=match).order_by('player__rank')
    return render_to_response(
        'tippspiel/match_detail.html',
        {
            'match': match,
            'tipps': tipps
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

@login_required
def settings(request):
    errors = []
    if request.method == 'POST':
        npw = 1
        npw_c = 1
    return render_to_response(
        'tippspiel/settings.html',
        {
            'errors': errors
        },
        context_instance=RequestContext(request)
    )


@staff_member_required
def update_scores_and_ranks(request):
    # update scores
    for player in Player.objects.all():
        player.update_score()
        player.save()

    # update ranks
    players = Player.objects.all().order_by('score').reverse()
    rank, tick, score = 1, 0, players[0].score
    for player in players:
        if player.score < score:
            rank += tick
            tick = 1
            score = player.score
        else:
            tick += 1
        if player.rank != rank:
            player.rank = rank
            player.save()

    return HttpResponseRedirect(reverse('tippspiel_settings'))
