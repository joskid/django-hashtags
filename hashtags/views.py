# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.template import loader, RequestContext
from django.views.generic import list_detail
from hashtag.models import Hashtag, HashtaggedItem

def hashtagged_item_list(request, hashtag, template_loader=loader,
                         template_name="hashtags/hashtagged_item_list",
                         extra_context={}, context_processors=None,
                         template_object_name='hashtagged_item_list',
                         mimetype=None):
    try:
        hashtag = Hashtag.object.get(name=hashtag)
    except ObjectDoesNotExist:
        raise Http404("Hashtag %s doesn't exist." % hashtag)
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'hashtag': hashtag,
        template_object_name: HashtaggedItem.objects.filter(hashtag=hashtag),
    }, context_processors)
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    return HttpResponse(t.render(c), mimetype=mimetype)

def hashtag_index(request, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.list_detail.object_list``.
    """
    if 'queryset' not in kwargs:
        kwargs['queryset'] = Hashtag.objects.all()
    if 'template_object_name' not in kwargs:
        kwargs['template_object_name'] = 'hashtag'
    return list_detail.object_list(request, *args, **kwargs)
