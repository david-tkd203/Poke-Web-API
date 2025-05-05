# pokemon/templatetags/pokemon_extras.py
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(text, query):
    text = escape(text)
    query = escape(query.lower())
    result = text.replace(query, f'<span class="search-highlight">{query}</span>')
    return mark_safe(result)