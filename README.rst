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


Views
-----

hashtag_index
`````````````
A thin wrapper around ``django.views.generic.list_detail.object_list``.
You don't need provide the ``queryset`` if you want.

The ``template_object_name`` by default is ``'hashtag'``. This mean that the
context variable ``object_list`` will be renamed to ``hashtag_list``.

**Template name**:

If ``template_name`` isn't specified, this view will use the template
``hashtags/hashtag_index.html`` by default.


See the `official documentation for
django.views.generic.list_detail.object_list
<http://docs.djangoproject.com/en/1.1/ref/generic-views/#django-views-generic-list-detail-object-list>`_.


hashtagged_item_list
````````````````````
A page representing a list of objects hastagged with ``hashtag``.

Works like ``django.views.generic.list_detail.object_list`` with the
peculiarities documented below.

**Required arguments**:

  * ``hashtag``: name of hashtag.

**Optional arguments**:

  * ``paginate_by``: An integer specifying how many objects should be displayed
    per page. If this is given, the view will paginate objects with paginate_by
    objects per page. The view will expect either a page query string parameter
    (via GET) or a page variable specified in the URLconf.

  * ``page``: The current page number, as an integer, or the string
    'last'. This is 1-based.

  * ``template_name``: The full name of a template to use in rendering the
    page. This lets you override the default template name. By default, it's
    ``hashtags/hashtagged_item_list.html``.

  * ``template_object_name``: Designates the name of the template variable to
    use in the template context. By default, this is
    ``'hashtagged_item_list'``.

  * ``extra_context``: A dictionary of values to add to the template
    context. By default, this is an empty dictionary. If a value in the
    dictionary is callable, the view will call it just before rendering the
    template.

  * ``allow_empty``: A boolean specifying whether to display the page if no
    objects are available. If this is ``False`` and no objects are available,
    the view will raise a 404 instead of displaying an empty page. By default,
    this is ``True``.

*Unlike the generic view ``object_list`` you don't provide a ``queryset`` but
a hashtag name in the URL.*

**Template name**:

If ``template_name`` isn't specified, this view will use the template
``hashtags/hashtagged_item_list.html`` by default.

In addition to ``extra_context``, the template's context will be:

  * ``hashtag``: The hashtag object in question.

  * ``hashtagged_item_list``: The list of objects hashtagged with ``hastag``.

  * ``is_paginated``: A boolean representing whether the results are
    paginated. Specifically, this is set to ``False`` if the number of
    available objects is less than or equal to ``paginate_by``.

If the results are paginated, the context will contain these extra variables:

  * ``paginator``: An instance of ``django.core.paginator.Paginator``.

  * ``page_obj``: An instance of ``django.core.paginator.Page``.


*Note: on directory "etc/sample_templates/" you have some template examples.*


Template tags
-------------

The ``hashtags.templatetags.hashtags_tags`` module defines a number of template
tags which may be used to work with hashtags.

To access Hashtags template tags in a template, use the {% load %}
tag::

    {% load hashtags_tags %}

urlize_hashtags filter
``````````````````````

Converts hashtags in plain text into clickable links.

For example::

    {{ value|urlize_hashtags }}

If value is "This is a #test.", the output will be::

    This is a <a href="[reversed url for hashtagged_item_list(request, hashtag='test')]">#test</a>.

Note that if ``urlize_hashtags`` is applied to text that already contains HTML
markup, things won't work as expected. Prefer apply this filter to plain text.

urlize_and_track_hashtags filter
````````````````````````````````

Works like ``urlize_hashtags`` but you can pass a object parameter to
link/relate hashtags on text with the object in question.

Usage example::

    {{ value|urlize_and_track_hashtags:object_to_track }}

Real world example::

    {{ flatpage.content|urlize_and_track_hashtags:flatpage }}

**Important**: ``urlize_and_track_hashtags`` doesn't works property if your
object has two fields with hashtags to be tracked. Use the signals below if you
want this feature or if you want hashtags updated on ``post_save`` signal
instead on template rendering.


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
    The actual instance being saved.
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
class attribute, then your ``post_save_handler`` can be::

    def post_save_handler(sender, instance, **kwargs):
        hashtagged_model_was_saved.send(sender=sender, instance=instance)


Contributing
============

If you find any problems in the code or documentation, please take 30 seconds
to fill out a issue `here <http://github.com/semente/django-hashtags/issues>`_.

The contributing with code or translation is MUCH-APPRECIATED. You feel free to
create forks or send patchs.

See AUTHORS file for a complete authors list of this application.

Thanks to `Interaction Consortium <http://interactionconsortium.com/>`_ for
sponsoring the project. Donate you too!


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
