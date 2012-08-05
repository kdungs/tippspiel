from django.template.defaultfilters import register
from django.utils.translation import ugettext_lazy as _

@register.simple_tag
def gravatar(player, size=120):
    return 'http://gravatar.com/avatar/%s?s=%d' % (player.gravatar_hash(), size)

@register.simple_tag
def gravatar_img(player, size=120):
    return '<img src="%s" alt="%s %s." />' % (
        gravatar(player, size),
        unicode(_('Gravatar for')),
        player.user.username
    )
