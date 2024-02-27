from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django.contrib.auth.models import User
from api.serializers import MovieSerializer, ReviewSerializer, UserSerializer
from movie_review.models import Movie, Review
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class MovieViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head']
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    model = Movie
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genres', 'metascore']

    pagination_class = PageNumberPagination
    page_size = 15

    def get_queryset(self):
        return Movie.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    model = Review
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie', 'user']

    def perform_create(self, serializer):
        # Access the user associated with the token
        user = self.request.user

        # Set the user as the user of the newly created review
        serializer.save(user=user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


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


@api_view(['POST'])
def register_user(request):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        User.objects.create_user(
            serialized.init_data['email'],
            serialized.init_data['username'],
            serialized.init_data['password']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)