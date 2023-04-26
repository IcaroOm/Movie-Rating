from rest_framework import viewsets
from api.serializers import MovieSerializer, ReviewSerializer
from movie_review.models import Movie, Review
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)


class MovieViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head']
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    model = Movie
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genres', 'metascore']


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    model = Review
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie', 'user']
