from django import forms
from django.forms import Textarea, TextInput


class BlogForm(forms.Form):
    title = forms.CharField(max_length=128,
                            widget=TextInput(attrs={'placeholder': 'Title text',
                                                    'style': 'width: 400px;',
                                                    'class': 'form-control'}))
    text = forms.CharField(widget=Textarea(attrs={'placeholder': 'Blog entry text',
                                                  'style': 'width: 600px;',
                                                  'class': 'form-control'}))
