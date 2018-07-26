from django.db import models
from django.conf import settings
from account.models import User
from post.models import Post


class Like(models.Model):

    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=False)
    post_id = models.ForeignKey(Post, related_name='likes', on_delete=False)
    count = models.IntegerField(default=0)

