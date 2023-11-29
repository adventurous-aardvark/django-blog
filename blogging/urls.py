from django.urls import path
# noinspection PyUnresolvedReferences, PyPackageRequirements
from . import views
from blogging.views import detail_view, list_view

app_name = "blogs"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:author>", list_view, name='blog_entries'),
    path("<str:author>/<int:pk_id>", detail_view, name='blog_detail'),
    # path("posts/", stub_view, name='blog_index')
]
