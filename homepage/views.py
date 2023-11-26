# from django.http import HttpResponse, Http404
from django.shortcuts import render


# noinspection PyUnresolvedReferences,PyPackageRequirements

def index(request):
    context = {'poll': '/poll', 'blog': '/blog'}

    return render(request, 'homepage/index.html', context)
    # return HttpResponse("Hello, world. You're at the polling index.")
