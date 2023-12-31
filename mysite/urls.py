"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    
"""
from django.contrib import admin
from django.urls import include, path
from blogging.feeds import AtomSiteBlogFeed, RssBlogFeed

urlpatterns = [
    path("", include("homepage.urls", namespace='home')),
    path("blog/", include("blogging.urls", namespace='blogs')),
    path("poll/", include("polling.urls", namespace='polls')),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("atom/blog", AtomSiteBlogFeed(), name="atom_blog_feed"),
    path("rss/blog", RssBlogFeed(), name="rss_blog_feed"),
    path("rss/blog/<str:author>", RssBlogFeed(), name="rss_blog_author_feed"),
]
