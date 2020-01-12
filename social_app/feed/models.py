from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User(), on_delete=models.CASCADE) #if a user is deleted, their posts are also deleted
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    #formatting the way our objects are displayed
    def __str__(self):
        return self.title

    #redirect newly created post to the post-detail page
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'id': self.pk})


    def toggle_like(self, user):

        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def total_likes(self):
        return self.likes.count()

    def get_likers(self):
        return self.likes.all()
