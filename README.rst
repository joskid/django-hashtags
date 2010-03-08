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

If value is ``This is a #test.``, the output will be ``This is a
<a href="[reversed url for hashtagged_item_list(request, hashtag='test')]">
#test</a>.``.

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
