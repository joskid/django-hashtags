# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

"""
**Django Hashtags** is a generic application for `Django Web Framework`_ to
help you publish content with hashtags (like twitter hashtags), in documents,
or comments, or wherever.

.. _`Django Web Framework`: http://www.djangoproject.com
"""

VERSION = (0, 1)

def get_version():
    """
    Returns the version as a human-format string.
    """
    return '.'.join([str(i) for i in VERSION])

__author__ = 'See the file AUTHORS.'
__license__ = 'GNU Lesser General Public License (GPL), Version 3'
__url__ = 'http://github.com/semente/django-hashtags'
__version__ = get_version()
