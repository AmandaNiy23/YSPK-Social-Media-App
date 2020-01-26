
from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a public response...', 'rows':2, 'cols':50}))
    class Meta:
        model = Comment
        fields = ('content',)

        # def __init__():
        #     #super(CommentForm, self).__init__(*args, **kwargs)
        #     self.fields['content'].attrs['columns'] = 20;
