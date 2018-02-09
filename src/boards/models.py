import math
from django.db import models
from django.utils.html import mark_safe
from markdown import markdown
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Board(models.Model):

    '''Docstring for Board. '''
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        '''TODO: Docstring for __str__.

        :param arg1: TODO
        :returns: TODO

        '''
        return self.name


    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()


    def get_last_post(self):
        return Post.objects.filter( 
                topic__board=self).order_by('-created_at').first()



class Topic(models.Model):

    '''Docstring for Topic. '''
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    topics_per_page = 20


    def __str__(self):
        return self.subject


    def get_page_count(self):
        count = self.posts.count()
        pages = count / self.topics_per_page
        return math.ceil(pages)


    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6


    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def set_topics_per_page(self, ipp):
        self.topics_per_page = ipp


class Post(models.Model):

    '''Docstring for Post. '''
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')


    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)


    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class Profile(models.Model):

    '''Docstring for Profile. '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    topics_per_page = models.PositiveIntegerField(default=20)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
