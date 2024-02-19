from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import login_auth_token, MovieViewSet, ReviewViewSet

router = DefaultRouter()

router.register('movies', MovieViewSet, basename='movies')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('login-auth-token/', login_auth_token, name='login-auth-token'),
    re_path(r'^', include(router.urls)),
]
