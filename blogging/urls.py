from django.urls import path
# noinspection PyUnresolvedReferences, PyPackageRequirements
from . import views
from blogging.views import detail_view

app_name = "blogs"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:username>", detail_view, name='blog_detail'),
]
