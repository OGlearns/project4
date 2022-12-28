from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now=True, null=False, blank=False)
    # posts = models.ForeignKey('Post', blank=True, null=True, related_name="user_posts", on_delete=models.CASCADE)
    USERNAME_FIELD: str
    def __str__(self):
        return f"{self.username}"
    pass


class Comment(models.Model):
    # post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, null=False, blank=False, verbose_name='')
    date = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, related_name='liked_users', null=True, blank=True)
    comments = models.ForeignKey(Comment, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self) -> str:
    #     return super().__str__()

    def __str__(self):
        return f"{self.content}"

class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField('User', related_name='following', blank=True, null=True)
    followers = models.ManyToManyField('User', related_name='followers', blank=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"
