from rest_framework.serializers import ModelSerializer
from . import models


class LikeSerializer(ModelSerializer):

    class Meta:
        fields = ['owner_id', 'post_id', 'count']
        model = models.Like


class PostSerializer(ModelSerializer):
    class Meta:
        fields = ['title', 'id']
        model = models.Post




