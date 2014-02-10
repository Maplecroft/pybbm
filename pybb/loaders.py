# import django deps
from django import template
from django.utils.importlib import import_module


# client template loader
class ClientTemplateLoader(object):
    """
        Custom client template loader that
        is used to store client templates on
        the request object
    """
    def __init__(self, client_templates):
        self.client_templates = client_templates

    def template(self, template_name):
        """
            Loads template
        """
        return template.loader.select_template(
            self.template_names(template_name)
        )

    def template_names(self, template_name):
        """
            Builds a list of directories to search
            for templates
        """
        if isinstance(template_name, basestring):
            template_name = [template_name]
        paths = self.template_dirs()
        final = []
        for t in template_name:
            for p in paths:
                final.append('%s/%s' % (p, t))
        final.extend(template_name)
        return final

    def template_dirs(self):
        """
            Returns a list of directories containing templates for a
            game with the passed code, media and client
        """
        paths = [self.client_templates]
        return paths


# permission decorator loader
class PermissionDecoratorLoader(object):
    """
        Loads and resolves permissions decorators
        that need to be applied to pybb views
    """
    def __init__(self, to_load=None):
        self.decorators = []
        self.to_load = to_load
        self.resolve_decorators()

    def resolve_decorators(self):
        """
            Resolves the decorators and appends them
            to the decorators property
        """
        for dec in self.to_load:
            self.decorators.append(
                self.import_dec(dec))

    def import_dec(self, dotted_path):
        """
            Imports decorator function from dotted path
        """
        dot = dotted_path.rfind('.')
        module, func = dotted_path[:dot], dotted_path[dot + 1:]
        return getattr(import_module(module), func)
