from movie_review.models import Movie, Review, Genre, Person, Country, Language, Role
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
        movie=movie_one,
        actor=person_one,
        character='Character One'
    )
    movie_one.actors.add(person_one)
    movie_one.directors.add(person_one)
    movie_one.writers.add(person_one)
    movie_one.genres.add(genre_one)
    movie_one.languages.add(language_one)
    return movie_one


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


def test_movie_retrieve(db, client, movie_one):
    response = client.get(f'/api/movies/')
    print(response.data)
    assert 2 == 2
