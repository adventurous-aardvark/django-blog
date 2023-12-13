# Baseline code from https://ordinarycoders.com/blog/article/django-rss-feeds,
# https://learndjango.com/tutorials/django-rss-feed-tutorial
# and https://docs.djangoproject.com/en/4.2/ref/contrib/syndication/ examples
#

from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import truncatewords
from django.utils.feedgenerator import Atom1Feed
from blogging.models import Post


class RssBlogFeed(Feed):
    title = "Latest blog entries from the users"
    link = ""
    description = "Latest blog posts"

    def get_object(self, request, **kwargs):

        # Since application is controlled, can assume parameters are well
        # known and not to expect unknown parameters. Two formats expected:
        # with and without an author name. Invalid author name will pop a
        # 404 error.
        if "author" in kwargs:
            return get_object_or_404(User, username=kwargs["author"]).id

        return None

    def items(self, obj):

        if obj is not None:
            return Post.objects.filter(author_id=obj).order_by("-published_at")[:10]

        return Post.objects.order_by("-published_at")[:10]

    def item_title(self, item):

        return item.title

    def item_description(self, item):

        return truncatewords(item.text, 20)

    def item_lastupdated(self, item):

        return item.updated_at


class AtomSiteBlogFeed(RssBlogFeed):
    feed_type = Atom1Feed
    subtitle = RssBlogFeed.description
