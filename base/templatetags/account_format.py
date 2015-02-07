from django.template import Library
from datetime import date


register = Library()

_13_years = 13*365

@register.filter
def eligible(value):
    return 'allowed' if (date.today() - value).days >= 13*365 else 'blocked'


@register.filter
def BizzFuzz(value):
    result = ''
    if not(value % 3):
        result += 'Bizz'
    if not(value % 5):
        result += 'Fuzz'
    return result if result else value