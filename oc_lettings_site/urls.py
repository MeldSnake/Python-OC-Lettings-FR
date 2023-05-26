from django.contrib import admin
from django.urls import path, include

from . import views


def trigger_error(*args, **kwargs):
    _ = 12 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('', views.index, name='index'),
    path('lettings/', include("lettings.urls", namespace="lettings")),
    path('profiles/', include("profiles.urls", namespace="profiles")),
    path('admin/', admin.site.urls),
]
