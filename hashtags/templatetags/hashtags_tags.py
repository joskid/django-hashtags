# -*- coding: utf-8 -*-
#
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

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from hashtags.utils import link_hashtags_to_model, search_twitter

register = template.Library()

def urlize_hashtags(value):
    """
    Converts hashtags in plain text into clickable links.

    For example::

      {{ value|urlize_hashtags }}

    If value is "This is a #test.", the output will be "This is a
    <a href="[reversed url for hashtagged_item_list(request, hashtag='test')]">#test</a>.".

    Note that if ``urlize_hashtags`` is applied to text that already contains
    HTML markup, things won't work as expected. Prefer apply this filter to
    plain text.
    """
    from hashtags.utils import urlize_hashtags
    return mark_safe(urlize_hashtags(value))
urlize_hashtags.is_safe = True
urlize_hashtags = stringfilter(urlize_hashtags)

def urlize_and_track_hashtags(value, object_to_track):
    """
    Works like ``urlize_hashtags`` but you can pass a object parameter to
    link/relate hashtags on text with the object in question.

    Usage example::

        {{ value|urlize_and_track_hashtags:object_to_track }}

    Real world example::

        {{ flatpage.content|urlize_and_track_hashtags:flatpage }}

    **Important**: ``urlize_and_track_hashtags`` doesn't works property if your
    object has two fields with hashtags to be tracked. Use the signals below if
    you want this feature or if you want hashtags updated on ``post_save``
    signal instead on template rendering.
    """
    link_hashtags_to_model(value, object_to_track)
    return mark_safe(urlize_hashtags(value))
urlize_and_track_hashtags.is_safe = True
urlize_and_track_hashtags = stringfilter(urlize_and_track_hashtags)

class TweetListNode(template.Node):
    def __init__(self, num, hashtag, var_name):
        self.num = int(num)
        self.hashtag = template.Variable(hashtag)
        self.var_name = var_name

    def render(self, context):
        try:
            hashtag = '#%s' % self.hashtag.resolve(context).name
        except template.VariableDoesNotExist:
            if not str(self.hashtag)[0] == '#':
                hashtag = '#%s' % str(self.hashtag)
            else:
                hashtag = str(self.hashtag)
        values = {'q': hashtag, 'rpp': self.num}
        try:
            context[self.var_name] = search_twitter(values)['results']
        except IOError:
            context[self.var_name] = None
        return ''

def do_get_hashtagged_tweets(parser, token):
    """
    Search for hashtagged tweets and populates the template context with a
    variable containing that result list, whose name is defined by the 'as'
    clause.

    Syntax::

        {% get_hashtagged_tweets [num] [hashtag] as [var_name] %}

    Example usage::

        {% get_hashtagged_tweets 10 #django-hashtags as tweet_list %}

    Hashtag can be a ``hashtags.models.Hashtag`` too::

        {% get_hashtagged_tweets 10 hashtag_obj as tweet_list %}

    """
    bits = token.split_contents()
    if len(bits) == 5:
        if bits[3] != 'as':
            raise template.TemplateSyntaxError, \
                "Third argument to '%s' tag must be 'as'" % bits[0]
        return TweetListNode(bits[1], bits[2], bits[4])
    else:
        raise template.TemplateSyntaxError, \
            "'%s' tag takes four arguments" % bits[0]

register.filter(urlize_hashtags)
register.filter(urlize_and_track_hashtags)
register.tag('get_hashtagged_tweets', do_get_hashtagged_tweets)
