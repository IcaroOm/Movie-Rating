from django.contrib.auth import authenticate
from rest_framework import viewsets
from api.serializers import MovieSerializer, ReviewSerializer
from movie_review.models import Movie, Review
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
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


@api_view(['POST'])
@permission_classes([AllowAny])
def login_auth_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user:
        token = Token.objects.get(user=user)
        return Response({'token': token.key})
    else:
        return Response(
            {'error': 'Credenciais inválidas'},
            status=status.HTTP_400_BAD_REQUEST,
        )
