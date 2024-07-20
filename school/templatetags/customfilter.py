from django import template

register = template.Library()

@register.filter(name='Short')
def Short(data):
    p=str(data).split(',')
    return p[0]