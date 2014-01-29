# import django deps
from django import template


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
