from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from .views import PostAPIViewSet

router = SimpleRouter()
router.register(r'post', PostAPIViewSet)


urlpatterns = [
    url(r'^post/', include('like.urls')),
]

urlpatterns += router.urls
