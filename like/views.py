from .serializer import LikeSerializer, PostSerializer
from .models import Like
from post.models import Post
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.generics import Http404
from rest_framework.response import Response
from rest_framework.request import clone_request


# Select PUT request with update method and rewrite get_query_set method
class LikeAPIView(ModelViewSet):
    permission_classes = (AllowAny,)
    lookup_field = 'title'
    serializer_class = PostSerializer

    """
    Check post instab
    """
    @action(methods=['put'], detail=True, permission_classes=[AllowAny])
    def like(self, request, title=None, *args, **kwargs):
        instance = self.get_object_or_none()
        self.serializer_class = LikeSerializer
        if instance:
            post_id = instance.id
            data = {'post_id': post_id, 'owner_id': self.request.user.id}
            count = Like.objects.filter(post_id=post_id, owner_id=self.request.user.id)
        else:
            return Response( "Not exist" ,status=status.HTTP_404_NOT_FOUND)
        if count.exists():
            data['count'] = count.values()[0]['count']+1
            serializer = LikeSerializer(count.get(), data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            data['count'] = 1
            serializer = LikeSerializer(None, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def unlike(self, request, title=None, *args, **kwargs):
        instance = self.get_object_or_none()
        self.serializer_class = LikeSerializer
        if instance:
            post_id = instance.id
            data = {'post_id': post_id, 'owner_id': self.request.user.id}
            count = Like.objects.filter(post_id=post_id, owner_id=self.request.user.id)
        else:
            return Response( "Not exist" ,status=status.HTTP_404_NOT_FOUND)
        if count.exists():
            data['count'] = count.values()[0]['count']-1
            if data['count'] == 0:
                count.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = LikeSerializer(count.get(), data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        title = self.kwargs.get(self.lookup_field)
        print(self.request.user)
        like = Post.objects.filter(title=title)
        return like

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise
