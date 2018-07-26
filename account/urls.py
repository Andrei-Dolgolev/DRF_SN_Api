from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from .views import UserAPIViewSet, authenticate_user

router = SimpleRouter()
router.register(r'user', UserAPIViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^obtain_token/$', authenticate_user),
]
