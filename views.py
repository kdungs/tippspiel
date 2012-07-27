from django.shortcuts import render_to_response, get_object_or_404
from tippspiel.models import Player, Team, Match, Tipp

def index(request):
    return render_to_response('tippspiel/index.html', {})

def player(request, player_name):
    p = get_object_or_404(Player, user__username=player_name)
    return render_to_response('tippspiel/player.html', {'player': p})
