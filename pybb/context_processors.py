# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pybb import defaults

__author__ = 'zeus'


def processor(request):
    context = {}
    for i in (
        'PYBB_DEFAULT_AVATAR_URL',
        'PYBB_MARKUP',
        'PYBB_DEFAULT_TITLE',
        'PYBB_ENABLE_ANONYMOUS_POST',
        # deprecated, should be used pybb_may_attach_files filter,
        # will be removed
        'PYBB_ATTACHMENT_ENABLE',
        'PYBB_AVATAR_WIDTH',
        'PYBB_AVATAR_HEIGHT',
    ):
        context[i] = getattr(defaults, i, None)

    context['PYBB_AVATAR_DIMENSIONS'] = '%sx%s' % (
        defaults.PYBB_AVATAR_WIDTH, defaults.PYBB_AVATAR_WIDTH)

    # custom  maplecroft code to handle multi client forums
    context['PYBB_CLIENT'] = getattr(request, 'pybb_client', getattr(
        defaults, 'PYBB_CLIENT', 'pybb'))
    context['PYBB_TEMPLATE'] = getattr(request, 'pybb_template', getattr(
        defaults, 'PYBB_TEMPLATE', None))
    client_title = getattr(request, 'pybb_default_title', None)
    if client_title:
        context['PYBB_DEFAULT_TITLE'] = client_title

    return context
