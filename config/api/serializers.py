from rest_framework import serializers
from django.contrib.auth.models import User
from movie_review.models import (
    Movie,
    Genre,
    Person,
    Language,
    Country,
    Role,
    Review,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        movie = data['movie']

        # Check if the user has already reviewed the movie
        existing_review = (
            Review.objects.filter(user=user, movie=movie)
            .exclude(pk=self.instance.pk if self.instance else None)
            .first()
        )

        if existing_review:
            raise serializers.ValidationError(
                'You have already reviewed this movie.'
            )

        return data


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    directors = PersonSerializer(many=True)
    writers = PersonSerializer(many=True)
    actors = serializers.SerializerMethodField()
    countries = CountrySerializer(many=False)
    languages = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def get_actors(self, obj):
        roles = obj.role_set.all()
        return [
            {'name': role.actor.name, 'character': role.character}
            for role in roles
        ]
