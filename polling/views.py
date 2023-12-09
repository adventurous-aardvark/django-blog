from django.http import Http404
from django.shortcuts import render
# noinspection PyUnresolvedReferences,PyPackageRequirements
from polling.models import Poll



def list_view(request):
    context = {'polls': Poll.objects.all}
    return render(request, 'polling/list.html', context)


def detail_view(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)

    except Poll.DoesNotExist:
        raise Http404('Invalid poll number')

    if request.method == 'POST':
        if request.POST.get('vote') == 'Yes':
            poll.score += 1
        else:
            poll.score -= 1  # Since binary choice no need to check for bad data
        poll.save()
    context = {'poll': poll}

    return render(request, 'polling/detail.html', context)


def index(request):
    context = {'polls': Poll.objects.all}

    return render(request, 'polling/index.html', context)
