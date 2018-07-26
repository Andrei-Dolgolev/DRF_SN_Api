from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('api/', include('account.urls')),
    url('api/', include('post.urls')),
]