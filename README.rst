===============
Django Hashtags
===============

**Django Hashtags** is a generic application for `Django Web Framework`_ to
help you publish content with hashtags (like twitter hashtags), in documents,
or comments, or wherever.

.. _`Django Web Framework`: http://www.djangoproject.com


Installing & Setup
==================

Hashtags is in the `Python Package Index (PyPI)`_ and you can easily install
the latest stable version of it using the tools ``pip`` or
``easy_install``. Try::

  pip install django-hashtags

or::

  easy_install django-hashtags

.. _`Python Package Index (PyPI)`: http://pypi.python.org


Alternatively, you can install Hashtags from source code running the follow
command on directory that contains the file ``setup.py``::

  python setup.py install

After installation you need configure your project to recognizes the Hashtags
application adding ``'hashtags'`` to your ``INSTALLED_APPS`` setting and this
pattern in your *URLConf*::

  (r'^hashtags/', include('hashtags.urls')),


Signals
-------

hashtagged_model_was_saved
``````````````````````````

A post-save signal hook to you connect function handlers to work with
hashtagged model fields.

Arguments sent with this signal:

sender
    The model class.
instance
    The actual instance being saved or updated.
hashtagged_field_list
    String list of the model fields that has hashtags to be tracked.
    Default: None

parse_fields_looking_for_hashtags
`````````````````````````````````

A function handler to work with ``hashtagged_model_was_saved`` signal. This
function parse a list of model fields looking for hashtags to be related/linked
with the model in question.

Usage example::

    # You need connect ``parse_fields_looking_for_hashtags`` on
    # ``hashtagged_model_was_saved`` only one time.
    from hashtags.signals import (hashtagged_model_was_saved,
                                  parse_fields_looking_for_hashtags)
    hashtagged_model_was_saved.connect(parse_fields_looking_for_hashtags)

Connecting your models that you want track hashtags (FlatPage example)::

    from django.contrib.flatpages.models import FlatPage
    from django.db.models.signals import post_save

    # connect hashtagged_model_was_saved signal to post_save
    def post_save_handler(sender, instance, **kwargs):
        hashtagged_model_was_saved.send(sender=sender, instance=instance,
            # put the hashtagged fields of your app here
            hashtagged_field_list=['title', 'content']
        )
    post_save.connect(post_save_handler, sender=FlatPage)

Alternatively you can set ``hashtagged_field_list`` in your model as a
class attribute, then your ``post_save_handler`` can be:

    def post_save_handler(sender, instance, **kwargs):
        hashtagged_model_was_saved.send(sender=sender, instance=instance)


Template tags
-------------

The ``hashtags.templatetags.hashtags_tags`` module defines a number of template
tags which may be used to work with hashtags.

To access Hashtags template tags in a template, use the {% load %}
tag::

    {% load hashtags_tags %}

urlize_hashtags
```````````````

Converts hashtags in plain text into clickable links.

For example::

    {{ value|urlize_hashtags }}

If value is "This is a #test.", the output will be::

    This is a <a href="[reversed url for hashtagged_item_list(request, hashtag='test')]">#test</a>.

Note that if ``urlize_hashtags`` is applied to text that already contains HTML
markup, things won't work as expected. Prefer apply this filter to plain text.


Copying conditions
==================

Django Hashtags is free software; you can redistribute it and/or modify it
under the terms of the `GNU Lesser General Public License`_ as published by the
Free Software Foundation; either version 3 of the License, or (at your option)
any later version.

Django Hashtags is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this program; see the file COPYING.LESSER. If not, see
http://www.gnu.org/licenses/.

.. _`GNU Lesser General Public License`: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
