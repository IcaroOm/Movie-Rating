from movie_review.models import Movie, Review, Genre, Person, Country, Language
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def auth_api_client(db):
    api_client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client, user


@pytest.fixture
def review_one(db, movie_one):
    return Review.object.create(
        movie=movie_one,
        user=auth_api_client.user,
        value=2,
        review='Review One test',
    )


def test_movies_healthcheck(db, client):
    response = client.get(f'/api/movies/')
    assert response.status_code == 200


def test_review_healthcheck(db, client):
    response = client.get(f'/api/reviews/')
    assert response.status_code == 200


def test_broken(db, client):
    assert 1 == 2
