from django.contrib import admin
from tippspiel.models import Player, Team, Match, Tipp

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Tipp)
