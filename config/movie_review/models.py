from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
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
    directors = models.ManyToManyField(
        'Person', related_name='directed_movies'
    )
    writers = models.ManyToManyField('Person', related_name='written_movies')
    actors = models.ManyToManyField(
        'Person', through='Role', related_name='movies'
    )
    countries = models.ForeignKey('Country', on_delete=models.CASCADE)
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


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:

        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.movie} - {self.value} - {self.created_at}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField('Staff', default=False)
    is_admin = models.BooleanField('Admin', default=False)
    is_reviewer = models.BooleanField('Reviewer', default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
    instance.profile.save()
