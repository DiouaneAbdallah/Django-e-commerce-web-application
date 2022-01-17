from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value*arg

@register.filter(name='div')
def div(value, arg):
    return value/arg

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='index')
def index(liste, elem):
    return liste.index(elem)

@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]
upto.is_safe = True

@register.filter(name='range')
def range(value,number):
	return value[:number]

@register.filter(name='numpages')
def numpages(paginator):
	return paginator.num_pages

@register.filter(name='count')
def count(paginator):
	return paginator.count

@register.filter(name='page')
def page(paginator,num):
	return paginator.page(num)
@register.filter
def hash(h, key):
    return h[key]
