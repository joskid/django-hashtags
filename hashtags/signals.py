# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.contrib.contenttypes.models import ContentType
from django.dispatch import Signal
from django.db.utils import IntegrityError
from hashtags.models import Hashtag, HashtaggedItem
from hashtags.utils import hashtag_pattern

hashtagged_model_was_saved = Signal(providing_args=['hashtagged_field_list'])

def parse_fields_looking_for_hashtags(sender, instance, hashtagged_field_list=None, **kwargs):
    if not hashtagged_field_list:
        try:
            hashtagged_field_list = sender.hashtagged_field_list
        except AttributeError:
            return

    # parsing fields looking for hashtags to be linked with the instance
    hashtag_list = []
    for field in hashtagged_field_list:
        for hname in hashtag_pattern.findall(instance.__getattribute__(field)):
            hashtag = Hashtag.objects.get_or_create(name=hname)
            hashtag_list.append(hashtag)

    # unlinking instance from old hashtags and purging unused hashtags
    instance_type = ContentType.objects.get_for_model(sender)
    qs = HashtaggedItem.objects.exclude(hashtag__in=hashtag_list)
    qs = qs.filter(content_type=instance_type, object_id=instance.id)
    old_hashtag_list = [item.hashtag for item in qs]
    for hashtag in old_hashtag_list:
        if hashtag.hashtaggeditem_set.all().count() == 1:
            hashtag.delete()
        else:
            HashtaggedItem.objects.get(hashtag=hashtag, object_id=instance.id,
                                       content_type=instance_type).delete()

    # linking instance to the new hashtags
    for hashtag in hashtag_list:
        try:
            HashtaggedItem(content_object=instance, hashtag=hashtag).save()
        except IntegrityError:
            continue
