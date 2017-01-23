from urllib.parse import quote

from django import template

register = template.Library()
#registers a custom filter, that quotes a value and can then be called from a temlate with |urlify
@register.filter
def urlify(value):
    return quote(value)
