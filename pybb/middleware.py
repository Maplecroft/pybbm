# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils import translation
from django.conf import settings
from django.db.models import ObjectDoesNotExist
from pybb import util
from pybb.loaders import ClientTemplateLoader, PermissionDecoratorLoader


class PybbMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                # Here we try to load profile, but can get error
                # if user created during syncdb but profile model
                # under south control. (Like pybb.Profile).
                profile = util.get_pybb_profile(request.user)
            except ObjectDoesNotExist:
                # Ok, we should create new profile for this user
                # and grant permissions for add posts
                # It should be caused rarely, so we move import signal here
                # to prevent circular import
                from pybb.models import user_saved
                user_saved(request.user, created=True)
                profile = util.get_pybb_profile(request.user)

            language = translation.get_language_from_request(request)

            if not profile.language:
                profile.language = language
                profile.save()

            if profile.language and profile.language != language:
                request.session['django_language'] = profile.language
                translation.activate(profile.language)
                request.LANGUAGE_CODE = translation.get_language()


class PybbRouterMiddleware(object):
    """
        VERY crude...
        Not impressed with this, but time limitations and needs must.

        This Middleware is designed to process the client we need to
        load the forums for based on the url. Ideally I would like to
        do this with request headers but we just need something running.
    """
    def process_request(self, request):
        request.pybb_client = None
        request.pybb_templates = None
        request.pybb_permission_decorators = None
        request.pybb_default_title = None
        if request.path:
            for path, config_data in settings.PYBB_CLIENT_FORUMS.items():
                if request.path.startswith(path):
                    request.pybb_client = config_data.get('client')
                    request.pybb_default_title = config_data.get(
                        'forum_title', None)
                    request.pybb_template = config_data.get('base_template')
                    request.pybb_client_templates = ClientTemplateLoader(
                        config_data.get('client_templates'))
                    if config_data.get('permission_decorators', None):
                        request.pybb_permission_decorators = \
                            PermissionDecoratorLoader(config_data.get(
                                'permission_decorators'))
                    break
