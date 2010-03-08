# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

"""
The ``hashtags.templatetags.hashtags_tags`` module defines a number of template
tags which may be used to work with hashtags.

To access Hashtags template tags in a template, use the {% load %}
tag::

    {% load hashtags_tags %}

"""

from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = Library()

def urlize_hashtags(value):
    """
    Converts hashtags in plain text into clickable links.

    For example::

      {{ value|urlize_hashtags }}

    If value is "This is a #test.", the output will be "This is a
    <a href="[reversed url for hashtagged_item_list(request, hashtag='test')]">
        #test</a>.".

    Note that if ``urlize_hashtags`` is applied to text that already contains
    HTML markup, things won't work as expected. Prefer apply this filter to
    plain text.
    """
    from hashtags.utils import urlize_hashtags
    return mark_safe(urlize_hashtags(value))
urlize_hashtags.is_safe = True
urlize_hashtags = stringfilter(urlize_hashtags)

register.filter(urlize_hashtags)
