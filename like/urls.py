from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<title>\w+)/like/$', views.LikeAPIView.as_view({'put':'like'}), name='like'),
    url(r'^(?P<title>\w+)/unlike/$', views.LikeAPIView.as_view({'put':'unlike'}), name='like'),
]