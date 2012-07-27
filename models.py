from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


class Player(models.Model):
    """A player is a user in the context of the tippspiel."""
    user = models.OneToOneField(User)
    score = models.IntegerField("The player's score.", default=0)
    rank = models.IntegerField("The player's rank", default=-1)

    def __unicode__(self):
        return self.user.username


# connect signal
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

post_save.connect(create_player, sender=User)



class Team(models.Model):
    """A team in the Bundesliga"""
    handle = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.handle



class Match(models.Model):
    """A match between two teams."""
    date = models.DateTimeField()
    matchday = models.IntegerField(default=0)
    team_home = models.ForeignKey(Team, related_name='+')
    team_visitor = models.ForeignKey(Team, related_name='+')
    score_home = models.IntegerField(default=-1)
    score_visitor = models.IntegerField(default=-1)

    def has_started(self):
        return self.date <= timezone.now()

    
    def __unicode__(self):
        return '%s %d:%d %s' % (self.team_home.handle, self.score_home, self.score_visitor, self.team_visitor.handle)



class Tipp(models.Model):
    """A bet by a player on a match."""
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    date = models.DateTimeField()
    score_home = models.IntegerField(default=0)
    score_visitor = models.IntegerField(default=0)

    def points(self):
        sh = self.match.score_home
        sv = self.match.score_visitor
        th = self.score_home
        tv = self.score_visitor
        if -1 in [sh, sv, th, tv]:
            return 0
        sgn = lambda x: 0 if x==0 else x/abs(x)
        points = 0
        ds = sh-sv
        dt = th-tv
        if sgn(ds)==sgn(dt):
            # correct tendency
            points += 1
            if ds==dt:
                # correct difference
                points += 1
                if sh==th:
                    # correct result
                    points += 1
        return points


    def __unicode__(self):
        return 'Tipp by %s on %s (%d:%d) (%d)' % (self.player, self.match, self.score_home, self.score_visitor, self.points())
