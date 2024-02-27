from movie_review.models import (
    Movie,
    Review,
    Genre,
    Person,
    Country,
    Language,
    Role,
)
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def user_test(db):
    user = User.objects.create_user(
        username='joca', password='minhasenhasecreta'
    )
    return user


@pytest.fixture
def client_review(db, user_test):
    api_client = APIClient()
    token = Token.objects.get(user=user_test)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    user_test.save()
    return api_client


@pytest.fixture
def token_test(db, user_test):
    token = Token.objects.get(user=user_test)
    return token


@pytest.fixture
def auth_api_client(db):
    api_client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client, user


@pytest.fixture
def movie_one(db):
    person_one = Person.objects.create(name='Name One')
    genre_one = Genre.objects.create(name='Genre One')
    country_one = Country.objects.create(name='Country One')
    language_one = Language.objects.create(name='Language One')
    movie_one = Movie.objects.create(
        title='Title One',
        year=2023,
        runtime=123,
        rating=9.9,
        votes=12_345,
        metascore=9.8,
        plot='Plot Movie One',
        tagline='tagline one',
        countries=country_one,
        budget=123_456_789,
        gross=987_654_321,
    )
    role_one = Role.objects.create(
        movie=movie_one, actor=person_one, character='Character One'
    )
    movie_one.actors.add(person_one)
    movie_one.directors.add(person_one)
    movie_one.writers.add(person_one)
    movie_one.genres.add(genre_one)
    movie_one.languages.add(language_one)
    return movie_one


@pytest.fixture
def review_one(db, movie_one, user_test):
    return Review.objects.create(
        movie=movie_one,
        user=user_test,
        value=2,
        review='Review One test',
    )


@pytest.fixture
def review_data(db, movie_one):
    return {
        "movie": "1",
        "value": "2",
        "review": "Review One test"
    }


def test_movies_healthcheck(db, client):
    response = client.get(f'/api/movies/')
    assert response.status_code == 200


def test_review_healthcheck(db, client):
    response = client.get(f'/api/reviews/')
    assert response.status_code == 200


def test_movie_retrieve(db, client, movie_one):
    response = client.get(f'/api/movies/')
    assert response.data[0]['title'] == movie_one.title


def test_review_retrieve(db, client, review_one):
    response = client.get(f'/api/reviews/')


def test_login_auth(db, user_test, token_test, client):
    data = {'username': 'joca', 'password': 'minhasenhasecreta'}
    response = client.post('/api/login-auth-token/', data=data)
    assert response.data['token'] == token_test.key


def test_login_declined(db, client):
    data = {'username': 'test', 'password': 'minhasenhaerrada'}
    response = client.post('/api/login-auth-token/', data=data)
    assert response.status_code == 400


def test_review_post(
    db, client_review, client, review_data, user_test, movie_one
):
    response_post = client_review.post('/api/reviews/', data=review_data)
    response_get = client.get('/api/reviews/')
    assert response_post.status_code == 201
    assert response_get.data[0]['value'] == 2.0
    assert response_get.data[0]['user'] == user_test.id


def test_review_post_declined(db, client, review_data):
    response = client.post('/api/reviews/', data=review_data)
    assert response.status_code == 401
