# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

import re
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode

hashtag_pattern = re.compile(r'[#]+([-_a-zA-Z0-9]+)')

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
