from django import forms
from django.forms import BooleanField, CharField, ChoiceField, Textarea, TextInput
from blogging.models import Category


class BlogForm(forms.Form):

    CATEGORY_CHOICES = []
    PUBLISH_CHOICE = [('Y', 'Yes'), ('N', 'No')]

    title = CharField(max_length=128,
                      widget=TextInput(attrs={'label': 'title',
                                              'initial': '',
                                              'placeholder': 'Title text',
                                              'style': 'width: 400px;',
                                              'class': 'form-control'}))

    text = CharField(max_length=1024,
                     widget=Textarea(attrs={'label': 'text',
                                            'initial': '',
                                            'placeholder': 'Blog entry text',
                                            'style': 'width: 600px; height: 100px;',
                                            'class': 'form-control'}))

    publish = BooleanField(label = 'publish',
                           required = False,
                           initial = True)

    # categories = \
    #    forms.ModelMultipleChoiceField(label = 'categories',
    #                                   queryset = Category.objects.all(),
    #                                   initial = 0)
