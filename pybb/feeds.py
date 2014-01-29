# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _

from pybb.models import Post, Topic

from pybb.permissions import perms


class PybbFeed(Feed):
    feed_type = Atom1Feed

    def link(self):
        """
            Just return an empty string for this
            since we need to return a namespaced link
            based on client. We do this by overriding
            the get_feed method instead.
        """
        return ''

    def get_namespaced_link(self, request, **kwargs):
        """
            Method that returns a namespaced reversed url
            based on the client in the request.
        """
        return reverse('%s_pybb:index' % request.pybb_client)

    def item_guid(self, obj):
        return str(obj.id)

    def item_pubdate(self, obj):
        return obj.created

    def get_feed(self, obj, request):
        """
            Override the ``get_feed`` method so that we can
            return a namespaced url based on the client in
            the request
        """
        feed = super(PybbFeed, self).get_feed(obj, request)
        feed.feed['link'] = self.get_namespaced_link(request)
        return feed


class LastPosts(PybbFeed):
    title = _('Latest posts on forum')
    description = _('Latest posts on forum')
    title_template = 'pybb/feeds/posts_title.html'
    description_template = 'pybb/feeds/posts_description.html'

    def get_object(self, request, *args, **kwargs):
        return request.user

    def items(self, user):
        ids = [p.id for p in perms.filter_posts(
            user, Post.objects.only('id')).order_by('-created')[:15]]
        return Post.objects.filter(id__in=ids).select_related(
            'topic', 'topic__forum', 'user')


class LastTopics(PybbFeed):
    title = _('Latest topics on forum')
    description = _('Latest topics on forum')
    title_template = 'pybb/feeds/topics_title.html'
    description_template = 'pybb/feeds/topics_description.html'

    def get_object(self, request, *args, **kwargs):
        return request.user

    def items(self, user):
        return perms.filter_topics(
            user, Topic.objects.all()).order_by('-created')[:15]
