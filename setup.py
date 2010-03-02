# Copyright (c) 2009 Guilherme Gondim and contributors
#
# This file is part of Django Hashtags.
#
# Django Hashtags is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from hashtags import get_version

setup(
    name = 'django-hashtags',
    version = get_version(),
    description = 'A generic hashtagging application for Django projects.',
    long_description = ('Django Hashtags is a generic application for Django '
                        'Web Framework to help you publish content with '
                        'hashtags (like twitter hashtags), in documents, or '
                        'comments, or wherever.'),
    keywords = 'django apps hashtag tagging',
    author = 'Guilherme Gondim',
    author_email = 'semente@taurinus.org',
    url = 'http://github.com/semente/django-hashtags',
    download_url = 'http://github.com/semente/django-hashtags/downloads',
    license = 'GNU Lesser General Public License (LGPL), Version 3',
    classifiers = [
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
)
