from django import template
from string import Template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.simple_tag
def activepage(request, url, title, icon=None):
    s = Template('<a href="$link"$active$icon>$title</a>')

    the_icon = ''
    if not icon is None:
        the_icon = ' data-icon="%s"' % icon

    active = ''
    if reverse(url) == request.path:
        active = ' class="ui-btn-active ui-state-persist"'

    return s.substitute(link=reverse(url), active=active, icon=the_icon, title=unicode(_(title)))

@register.simple_tag
def activepage_with_icon(request, url, title, icon):
    return activepage(request, url, title, icon)
