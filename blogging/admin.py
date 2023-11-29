from django.contrib import admin
# noinspection PyUnresolvedReferences, PyPackageRequirements

from blogging.models import Category, Post

admin.site.register(Category)
admin.site.register(Post)

# Register your models here.
