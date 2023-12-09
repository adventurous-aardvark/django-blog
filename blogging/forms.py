from django import forms
from django.forms import BooleanField, CharField, MultipleChoiceField, Textarea, TextInput


class BlogForm(forms.Form):
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

    publish = BooleanField(label='publish',
                           required=False,
                           initial=True)

    category = MultipleChoiceField(label='category',
                                   required=False,
                                   choices=())

    def __init__(self, *args, **kwargs):
        category_choices = kwargs.pop('category_choices', ())
        initial_set = kwargs.pop('initial_tags', [])
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = category_choices
        self.fields['category'].initial = initial_set

    class Meta:
        fields = ('title', 'text', 'publish', 'category')
