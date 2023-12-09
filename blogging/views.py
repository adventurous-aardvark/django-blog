"""
    Application views for blogs using classes.
"""

from html import escape
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import ListView
from blogging.models import Category, Post
from blogging.forms import BlogForm


# pylint: disable=W0613

class BlogDetailView(ListView):
    http_method_names = ['get', 'post']
    model = Post
    template_name = 'blogging/detail.html'

    def get_category_tags(self) -> tuple:
        """
        Generates an ordered by name collection of tuples that identifies the
        database ID as string for a category tag and the name text associated
        with the tag. Output intened to be supplied to the Multiple Category
        Selection object.

        Returns:
            tuple: Tuple list of category tags ordered as tag id, tag name.

        """

        category_tags = [('-1', '-- Optionally select one or more tags below --')]
        for cat in Category.objects.order_by('name'):
            category_tags.append((str(cat.id), cat.name))

        return tuple(category_tags)

    def get_post_tags(self, post: Post) -> list:
        """
        Create a list of strings representing the database ID number for the
        tag categories set in the post.

        Args:
            post (Post): Post to read the category values for.

        Returns:
            list: List of set tags in post as strings.

        """

        tag_list = []
        set_tags = post.categories.all()
        for tag in set_tags:
            tag_list.append(str(tag.id))

        return tag_list

    def get_context_data(self, **kwargs):
        """
        Setup the context data for rendering. Since the templates are complex
        and pull both database information and derived information, cannot use
        all of the built-in features of the ListView class.
        """

        author = self.kwargs["author"]
        author = escape(author)

        user = get_object_or_404(User, username=author)
        if (user.first_name == "") or (user.last_name == ""):
            show_name = user.username
        else:
            show_name = f"{user.first_name} {user.last_name}"

        post = get_object_or_404(Post, id=self.kwargs["post_id"])

        if post.author.id == user.id:
            form = BlogForm(initial={'title': post.title,
                                     'text': post.text,
                                     'publish': post.published_at is not None},
                            category_choices=self.get_category_tags(),
                            initial_tags=self.get_post_tags(post))

            context = super().get_context_data(**kwargs)
            context["user"] = user
            context["show_as"] = show_name
            context['post'] = post
            context["form"] = form

            return context

        raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        """
        Process POST operations from web browser
        """

        pk_id = self.kwargs["post_id"]
        post = get_object_or_404(Post, id=pk_id)

        if request.user.is_authenticated:
            form = BlogForm(request.POST,
                            category_choices=self.get_category_tags())

            if form.is_valid():
                if not form.cleaned_data['publish']:
                    post.published_at = None
                else:
                    if post.published_at is None:
                        post.published_at = timezone.now()
                post.title = form.cleaned_data['title']
                post.text = form.cleaned_data['text']
                post.update_at = timezone.now()
                post.save()

                tag_selections = form.cleaned_data['category']
                post.categories.clear()
                for tag in Category.objects.all():
                    if str(tag.id) in tag_selections:
                        post.categories.add(tag)

            else:
                print("*** Invalid form data ***")

        else:
            return HttpResponseForbidden('Not authorized')

        return redirect(request.META['HTTP_REFERER'])


class BlogIndexView(TemplateResponseMixin, View):
    template_name = 'blogging/index.html'

    def get_queryset(self):
        return User.objects.values()

    def get(self, request):
        queryset = self.get_queryset()
        user_list = []
        for person in queryset:
            user_list.append({'username': person['username'],
                              'first_name': person['first_name'],
                              'last_name': person['last_name']})

        context = {'users': user_list}
        return self.render_to_response(context)


class BlogListView(ListView):
    http_method_names = ['get', 'post']
    model = Post
    template_name = 'blogging/list.html'

    def get_category_tags(self) -> tuple:
        """
        Generates an ordered by name collection of tuples that identifies the
        database ID as string for a category tag and the name text associated
        with the tag

        Returns:
            tuple: Tuple list of category tags ordered as tag id, tag name.

        """

        category_tags = [('-1', '-- Optionally select one or more tags below --')]
        for cat in Category.objects.order_by('name'):
            category_tags.append((str(cat.id), cat.name))

        return tuple(category_tags)

    def get_context_data(self, **kwargs):
        """
        Setup the context data for rendering. Since the templates are complex
        and pull both database information and derived information, cannot use
        all of the built-in features of the ListView class.
        """

        author = self.kwargs["author"]
        author = escape(author)
        user = get_object_or_404(User, username=author)
        if (user.first_name == "") or (user.last_name == ""):
            show_name = user.username
        else:
            show_name = f"{user.first_name} {user.last_name}"

        # Cannot really use a query set as there this user blog entries to
        # display are supplied in the URL as a name which then maps to a
        # a primary_key value which in turn selects the author in the blogs.
        # Complicating this is that the data has to be sorted and filtered
        # based on if the user owns the data (all data viewed) or the user
        # is only viewing the data. The former is sorted by create date while
        # the latter is sorted by when updated (most recent first). To add to
        # the process, the returned context notes how many entries exist so
        # has to be counted by type. Since do not have access to the request
        # information which supplies web user ID, both lists are returned.
        # The actual determination of which list to show is determined by the
        # template.

        # Posts owned by the user (all)
        post_collection = Post.objects.filter(author=user.id)
        posts_created = post_collection.order_by('-created_at')
        post_count_created = posts_created.count()
        # For posts viewable by guest/not owner (filtered)
        post_collection = \
            Post.objects.exclude(published_at__exact=None).filter(author=user.id)
        posts_published = post_collection.order_by('-update_at')
        post_count_published = posts_published.count()

        context = super().get_context_data(**kwargs)
        context["user"] = user
        context["show_as"] = show_name
        context["posts_created"] = posts_created
        context["post_count_created"] = post_count_created
        context["posts_published"] = posts_published
        context["post_count_published"] = post_count_published
        context["form"] = BlogForm(category_choices=self.get_category_tags())

        return context

    def post(self, request, *args, **kwargs):
        """
        Process POST operations from web browser
        """

        if request.user.is_authenticated:
            form = BlogForm(request.POST,
                            initial={'publish': 'Yes'},
                            category_choices=self.get_category_tags())

            if form.is_valid():
                if form.cleaned_data['publish']:
                    publish_date = timezone.now()
                else:
                    publish_date = None

                new_post = Post(title=form.cleaned_data['title'],
                                text=form.cleaned_data['text'],
                                author=request.user,
                                published_at=publish_date)
                new_post.save()
                tag_selections = form.cleaned_data['category']
                for tag in Category.objects.all():
                    if str(tag.id) in tag_selections:
                        new_post.categories.add(tag)

            else:
                print("*** Invalid form data ***")

        else:
            return HttpResponseForbidden('Not authorized')

        return redirect(request.META['HTTP_REFERER'])


def stub_view(request, *args, **kwargs):
    """
    Diagnostic stub demonstrated in class.
    """

    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join([f"\t{a}" for a in args])

    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join([f"\t{a}" for a in kwargs.items()])

    return HttpResponse(body, content_type="text/plain")
