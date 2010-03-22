# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

import re
import simplejson
import urllib
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.utils.encoding import force_unicode
from hashtags.models import Hashtag, HashtaggedItem

hashtag_pattern = re.compile(r'[#]+([-_a-zA-Z0-9]+)')

def link_hashtags_to_model(text, object):
    # parsing text looking for hashtags to be linked with the object
    hashtag_list = []
    for hname in hashtag_pattern.findall(force_unicode(text)):
        hashtag, created = Hashtag.objects.get_or_create(name=hname)
        if created:
            hashtag.save()
        hashtag_list.append(hashtag)

    # unlinking object from old hashtags and purging unused hashtags
    object_type = ContentType.objects.get_for_model(object)
    qs = HashtaggedItem.objects.all().exclude(hashtag__in=hashtag_list)
    qs = qs.filter(content_type=object_type, object_id=object.id)
    old_hashtag_list = [item.hashtag for item in qs]
    for hashtag in old_hashtag_list:
        if hashtag.hashtaggeditem_set.all().count() == 1:
            hashtag.delete()
        else:
            HashtaggedItem.objects.get(hashtag=hashtag, object_id=object.id,
                                       content_type=object_type).delete()

    # linking object to the new hashtags
    for hashtag in hashtag_list:
        try:
            HashtaggedItem(content_object=object, hashtag=hashtag).save()
        except IntegrityError:
            continue

def search_twitter(values):
    url = 'http://search.twitter.com/search.json'
    values = urllib.urlencode(values)
    response = urllib.urlopen(url, values)
    return simplejson.load(response)

def urlize_hashtags(text):
    """
    Converts hashtags in plain text into clickable links.

    For example, if value of ``text`` is "This is a #test.", the output will be::

      This is a
      <a href="[reversed url for hashtagged_item_list(request, hashtag='test')]">
          #test</a>.

    Note that if the value of ``text`` already contains HTML markup, things
    won't work as expected. Prefer use this with plain text.
    """
    def repl(m):
        hashtag = m.group(1)
        url = reverse('hashtagged_item_list', kwargs={'hashtag': hashtag})
        return '<a href="%s">&#35;%s</a>' % (url, hashtag)
    return hashtag_pattern.sub(repl, force_unicode(text))
