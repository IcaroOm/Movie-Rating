from django.db import models

# Create your models here.
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    runtime = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)
    metascore = models.IntegerField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    tagline = models.CharField(max_length=200, null=True, blank=True)
    genres = models.ManyToManyField('Genre', related_name='movies')
    directors = models.ManyToManyField('Person', related_name='directed_movies')
    writers = models.ManyToManyField('Person', related_name='written_movies')
    actors = models.ManyToManyField('Person', through='Role', related_name='movies')
    countries = models.ManyToManyField('Country', related_name='movies')
    languages = models.ManyToManyField('Language', related_name='movies')
    budget = models.BigIntegerField(null=True, blank=True)
    gross = models.BigIntegerField(null=True, blank=True)

    # add more fields as needed

    def __str__(self):
        return f'{self.title} ({self.year})'


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Person, on_delete=models.CASCADE)
    character = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.actor} as {self.character} in {self.movie}'


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
