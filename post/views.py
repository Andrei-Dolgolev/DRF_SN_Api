from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CreatePostSerializer, PostSerializer,PostListSerializer
from .permissions import AnonlistAndUpdateOwnerOnlyAndAuthRetrieve
from .models import Post
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from .pagination import PostPageNumberPagination


class PostAPIViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (AnonlistAndUpdateOwnerOnlyAndAuthRetrieve,)
    lookup_field = 'title'
    pagination_class = PostPageNumberPagination  # PageNumberPagination

    """
    Calling after serializer.is_valid()
    """
    def perform_create(self, serializer):
        try:
            content_preview = self.request.data['content'][:200]
        except:
            content_preview = self.request.data['content']
        serializer.save(**{'owner': self.request.user,
                           'content_preview': content_preview})

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        if self.action == 'create':
            return CreatePostSerializer
        return PostSerializer
