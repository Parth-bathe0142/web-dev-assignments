from django import forms

from .models import Forum, Post

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Forum name",
                    "autocomplete": "off",
                }
            ),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["message"]

        widgets = {
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Write your post...",
                    "rows": 5,
                }
            ),
        }