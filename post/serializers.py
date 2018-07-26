from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from django.db.models import Sum
from . import models


# Post detail
class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='post-detail',lookup_field='title')
    owner = SerializerMethodField()
    img = SerializerMethodField()
    like_count = SerializerMethodField()

    class Meta:
        fields = ['owner','title', 'content_preview', 'url', 'img', 'like_count']
        model = models.Post

    def get_owner(self, obj):
        return str(obj.owner.first_name)

    def get_img(self, obj):
        try:
            img = obj.img.url
        except:
            img = None
        return img

    def get_like_count(self, obj):
       return obj.likes.filter(post_id=obj.id).aggregate(s=Sum('count'))['s']


# post
class PostSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='post-detail',lookup_field='title')
    owner = SerializerMethodField()
    img = SerializerMethodField()
    like_count = SerializerMethodField()

    class Meta:
        fields = ['owner', 'title', 'content', 'created_at', 'updated_at', 'url', 'img', 'like_count']
        model = models.Post
        extra_kwargs = {'created_at': {'read_only': True}}

    def get_owner(self, obj):
        return str(obj.owner.first_name)

    def get_img(self, obj):
        try:
            img = obj.img.url
        except:
            img = None
        return img

    def get_like_count(self, obj):
       return obj.likes.filter(post_id=obj.id).aggregate(s=Sum('count'))['s']


class CreatePostSerializer(ModelSerializer):

    class Meta:
        fields = ['title', 'content']
        model = models.Post
