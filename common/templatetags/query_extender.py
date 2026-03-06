import urllib.parse

from django.template import  Library

register = Library()
@register.simple_tag(takes_context=True)
def query_extender(context,key,value):
    dict_: dict=context["request"].GET.copy()
    dict_[key]=value
    return "?" + urllib.parse.urlencode(dict_)  #return urlib.parse.urlencode(_dict)