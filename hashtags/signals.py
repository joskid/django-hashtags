# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

"""
Signals relating to hashtags
"""

from django.contrib.contenttypes.models import ContentType
from django.dispatch import Signal
from django.db.utils import IntegrityError
from hashtags.models import Hashtag, HashtaggedItem
from hashtags.utils import hashtag_pattern

# A post-save signal hook to you connect function handlers to work with
# hashtagged model fields.
hashtagged_model_was_saved = Signal(providing_args=['hashtagged_field_list'])

def parse_fields_looking_for_hashtags(sender, instance, hashtagged_field_list=None, **kwargs):
    """
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

    """
    if not hashtagged_field_list:
        try:
            hashtagged_field_list = sender.hashtagged_field_list
        except AttributeError:
            return

    # parsing fields looking for hashtags to be linked with the instance
    hashtag_list = []
    for field in hashtagged_field_list:
        for hname in hashtag_pattern.findall(instance.__getattribute__(field)):
            hashtag, created = Hashtag.objects.get_or_create(name=hname)
            if created:
                hashtag.save()
            hashtag_list.append(hashtag)

    # unlinking instance from old hashtags and purging unused hashtags
    instance_type = ContentType.objects.get_for_model(sender)
    qs = HashtaggedItem.objects.all().exclude(hashtag__in=hashtag_list)
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
