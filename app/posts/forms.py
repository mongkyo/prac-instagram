from django import forms

from .models import Post


class PostCreateForm(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def save(self, author):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            author=author,
        )
        return post
