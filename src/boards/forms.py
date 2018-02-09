from django import forms
from django.contrib.auth.models import User
from .models import Topic, Post, Profile

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
            widget=forms.Textarea(
                attrs={'rows': 5, 'placeholder': 'What is on your mind?'}), 
            max_length=4000,
            help_text='The max length of the text is 4000.')

    class Meta:
        model = Topic
        fields = ['subject', 'message']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('topics_per_page', 'location', 'birth_date')
