from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
# noinspection PyUnresolvedReferences,PyPackageRequirements
from blogging.models import Post
from blogging.forms import BlogForm


def detail_view(request, author: str, pk_id: int):
    """
    Simple blog entry view for users not the author of the blog post.
    """

    try:
        user = User.objects.get(username=author)
        if (user.first_name == "") or (user.last_name == ""):
            show_name = user.username
        else:
            show_name = f"{user.first_name} {user.last_name}"
        post = Post.objects.get(pk=pk_id)

    except User.DoesNotExist:
        return HttpResponseNotFound('User or post not found')

    if request.method == "POST":
        if request.user.is_authenticated:
            form = BlogForm(request.POST)
            if form.is_valid():
                if not form.cleaned_data['publish']:
                    post.published_at = None
                else:
                    if post.published_at is None:
                        post.published_at = timezone.now()
                post.title = form.cleaned_data['title']
                post.text = form.cleaned_data['text']
                # post.categories = form.cleaned_data['categories']
                post.update_at = timezone.now()
                post.save()
            else:
                print('*** NOT VALID ***')

        else:
            return HttpResponseForbidden('Not authorized')
    else:
        if post.published_at is not None:
            publish = True
        else:
            publish = False
        form = BlogForm(initial={'title': post.title,
                                 'text': post.text,
                                 'publish': publish})
    #        ,
    #                                 'categories': post.categories})

    context = {'show_as': show_name,
               'user': user,
               'post': post,
               "form": form}

    return render(request, 'blogging/detail.html', context)


def index(request):
    user_list = []
    User = get_user_model()
    for person in User.objects.values():
        user_list.append({'username': person['username'],
                          'first_name': person['first_name'],
                          'last_name': person['last_name']})

    context = {'users': user_list, 'teststr': 'hello world'}

    return render(request, 'blogging/index.html', context)


@csrf_protect
def list_view(request, author: str):
    try:
        user = User.objects.get(username=author)
        if (user.first_name == "") or (user.last_name == ""):
            show_name = user.username
        else:
            show_name = f"{user.first_name} {user.last_name}"

    except User.DoesNotExist:
        return HttpResponseNotFound('User not found')

    if request.method == "POST":
        if request.user.is_authenticated:
            form = BlogForm(request.POST, initial={'publish': 'Yes'})
            if form.is_valid():
                if form.cleaned_data['publish'] == 'Y':
                    publish_date = timezone.now()
                else:
                    publish_date = None

                new_post = Post(title=form.cleaned_data['title'],
                                text=form.cleaned_data['text'],
                                author=request.user,
                                published_at=publish_date)
                new_post.save()

        else:
            return HttpResponseForbidden('Not authorized')

    if request.user.username == author:
        post_collection = Post.objects.filter(author=user)
        posts = post_collection.order_by('-created_at')
    else:
        post_collection = \
            Post.objects.exclude(published_at__exact=None).filter(author=user)
        posts = post_collection.order_by('-published_at')
    post_count = posts.count()

    context = {'show_as': show_name,
               'user': user,
               'posts': posts,
               'post_count': post_count,
               "form": BlogForm()}

    return render(request, 'blogging/list.html', context)


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
