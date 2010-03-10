# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponse
from django.template import loader, RequestContext
from django.views.generic import list_detail
from hashtags.models import Hashtag, HashtaggedItem

def hashtag_index(request, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.list_detail.object_list``.
    You don't need provide the ``queryset`` if you want.

    The ``template_object_name`` by default is ``'hashtag'``. This mean that the
    context variable ``object_list`` will be renamed to ``hashtag_list``.

    **Template name**:

    If ``template_name`` isn't specified, this view will use the template
    ``hashtags/hashtag_index.html`` by default.
    """
    if 'queryset' not in kwargs:
        kwargs['queryset'] = Hashtag.objects.all()
    if 'template_name' not in kwargs:
        kwargs['template_name'] = 'hashtags/hashtag_index.html'
    if 'template_object_name' not in kwargs:
        kwargs['template_object_name'] = 'hashtag'
    return list_detail.object_list(request, *args, **kwargs)

def hashtagged_item_list(request, hashtag, paginate_by=None, page=None,
                         allow_empty=True, template_loader=loader,
                         template_name="hashtags/hashtagged_item_list.html",
                         extra_context={}, context_processors=None,
                         template_object_name='hashtagged_item_list',
                         mimetype=None):
    """
    A page representing a list of objects hastagged with ``hashtag``.

    Works like ``django.views.generic.list_detail.object_list`.

    Templates: ``hashtags/hashtagged_item_list.html``
    Context:
        hashtag
            The hashtag object in question
        hashtagged_item_list
            The list of objects hashtagged with ``hastag``
        paginator
            An instance of ``django.core.paginator.Paginator``
        page_obj
            An instance of ``django.core.paginator.Page``
    """
    try:
        hashtag = Hashtag.objects.get(name=hashtag)
    except ObjectDoesNotExist:
        raise Http404("Hashtag %s doesn't exist." % hashtag)
    queryset = HashtaggedItem.objects.filter(hashtag=hashtag)
    if paginate_by:
        paginator = Paginator(queryset, paginate_by,
                              allow_empty_first_page=allow_empty)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int.
                raise Http404
        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            raise Http404
        c = RequestContext(request, {
            'hashtag': hashtag,
            template_object_name: queryset,
            'paginator': paginator,
            'page_obj': page_obj,
        }, context_processors)
    else:
        c = RequestContext(request, {
            'hashtag': hashtag,
            template_object_name: queryset,
            'paginator': None,
            'page_obj': None,
        }, context_processors)
        if not allow_empty and len(queryset) == 0:
            raise Http404
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    t = template_loader.get_template(template_name)
    return HttpResponse(t.render(c), mimetype=mimetype)
