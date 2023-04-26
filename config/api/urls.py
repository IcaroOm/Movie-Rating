from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register('movies', views.MovieViewSet, basename='movies')
router.register('reviews', views.ReviewViewSet, basename='reviews')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
