from django import template
from urllib.parse import urlencode, parse_qsl

register = template.Library()

@register.filter
def urlencode_page(querystring, key):
    """
    Remove a key (usually 'page') from the query string.
    """
    if not querystring:
        return ''
    params = dict(parse_qsl(querystring))
    params.pop(key, None)
    return urlencode(params)
