from django import forms
from django.forms import ModelForm
from .models import Post, Comment, Reply

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'created_at','likes']
        labels = {
            'title': 'Title',
            'image': 'Image URL',
            'body': 'Caption',
            'tags': 'Category'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter post title...',
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent'
            }),
            'image': forms.URLInput(attrs={
                'placeholder': 'https://example.com/image.jpg',
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent'
            }),
            'body': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your caption here...',
                'class': 'font1 text-4xl w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-checkbox text-primary rounded focus:ring-primary'
            }),
        }
        
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add Comment...',
                'class': 'w-full flex-1 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all'
            })
        }
        labels = {
            'body': ''
        }

class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add Reply...',
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all'
            })
        }
        labels = {
            'body': '',
        }