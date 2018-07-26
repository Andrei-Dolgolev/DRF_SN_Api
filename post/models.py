from django.db import models
from account.models import User
from django.db.models import Sum


class Post(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True,unique=True)
    owner = models.ForeignKey(User , on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=50)
    #img = models.ImageField()
    content_preview = models.TextField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_capacity(self):
        return self.likes.filter(post_id=self.id).aggregate(s=Sum('count'))['s']

    def __str__(self):
        return self.title