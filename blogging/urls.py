from django.urls import path
# noinspection PyUnresolvedReferences, PyPackageRequirements
from blogging.views import BlogDetailView, BlogIndexView, BlogListView


app_name = "blogs"
urlpatterns = [
    path("", BlogIndexView.as_view(), name="index"),
    path("<str:author>", BlogListView.as_view(), name="blog_entries"),
    path("<str:author>/<int:post_id>", BlogDetailView.as_view(), name="blog_detail"),
]
