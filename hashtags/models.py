# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Hashtag(models.Model):
    name = models.SlugField(
        _('name'),
        max_length=64,
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('hashtag')
        verbose_name_plural = _('hashtags')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('hashtag_detail', None, {'hashtag': str(self.name)})
    get_absolute_url = models.permalink(get_absolute_url)

class HashtaggedItem(models.Model):
    hashtag = models.ForeignKey(Hashtag)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('hashtag', 'content_type', 'object_id')
        verbose_name = _('hashtagged item')
        verbose_name_plural = _('hashtagged items')

    def __unicode__(self):
        return u'%s [%s]' % (self.content_object, self.hashtag)
