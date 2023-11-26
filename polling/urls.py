from django.urls import path
# noinspection PyUnresolvedReferences, PyPackageRequirements
from . import views
from polling.views import list_view, detail_view

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("current/", list_view, name='poll_index'),
    path("current/<int:poll_id>", detail_view, name='poll_detail'),
]
