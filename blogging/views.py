from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
# noinspection PyUnresolvedReferences,PyPackageRequirements
from blogging.models import Post
from blogging.forms import BlogForm


@csrf_protect
def detail_view(request, username):
    try:
        user = User.objects.get(username=username)
        if (user.first_name == "") or (user.last_name == ""):
            show_name = user.username
        else:
            show_name = f"{user.firstname} {user.last_name}"

    except User.DoesNotExist:
        return HttpResponseNotFound('User not found')

    if request.method == "POST":
        if request.user.is_authenticated:
            form = BlogForm(request.POST)
            if form.is_valid():
                new_post = Post(title=form.cleaned_data['title'],
                                text=form.cleaned_data['text'],
                                author=request.user)
                new_post.save()

        else:
            return HttpResponseForbidden('Not authorized')

    context = {'show_as': show_name,
               'user': user,
               'blogs': Post.objects.all(),
               "form": BlogForm()}

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
