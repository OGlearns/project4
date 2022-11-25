from . import models
from django import forms
from django.forms import ModelForm, TextInput, EmailInput

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