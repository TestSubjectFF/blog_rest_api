from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, help_text='Post title')
    text = models.TextField(help_text='Content of the comment')
    created = models.DateTimeField(auto_now_add=True,
                                   help_text='Creation date and time of \
                                   the post.')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             help_text='Post to which the comment relates.')
    username = models.CharField(max_length=50,
                                help_text='The name of the user, that created \
                                the comment.')
    text = models.CharField(max_length=500, help_text='Content of the comment')
    created = models.DateTimeField(auto_now_add=True,
                                   help_text='Creation date and time of \
                                   the comment.')

    def __str__(self):
        return f'{self.username}: {self.text}'
