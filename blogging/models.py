# Code segments on slugs from https://learndjango.com/tutorials/django-slug-tutorial
# with slight modifications to incorporate UUIDs
#

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=150, null=True)
    text = models.TextField(blank=True)
    categories = models.ManyToManyField(Category,
                                        blank=True,
                                        related_name='categories')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        post = get_object_or_404(Post, slug=str(self.slug))
        post_id = post.id
        author = User.objects.get(id=post.author_id).username
        url_fields = {"author": author, "post_id": post_id}

        return reverse("blogs:blog_detail", kwargs=url_fields)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Deviation from the tutorial. This allows for duplicate titles
            # across the pool of user blog entries, but does not cause a URL
            # collision.
            self.slug = slugify(self.title)[:91] + '-' + str(uuid.uuid4())
        return super().save(*args, **kwargs)
