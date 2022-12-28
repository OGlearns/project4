from . import models
from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from django.forms import modelformset_factory


class NewPostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['content']
        widgets = {
            'content' : TextInput(attrs={
                'class' : "form-control",
                'style' : "max-width: 100%;",
                'placeholder' : "Create a post.."
                            })
        }


class EditPostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['content']
        widgets = {
            'new_content': TextInput(attrs={
                'class' : "form-control",
                'style' : "max-width: 100%;",
                'placeholder' : "Save post.."
                            })
        }


EditPostFormSet = modelformset_factory(
    models.Post, fields=('content',), extra=1
)