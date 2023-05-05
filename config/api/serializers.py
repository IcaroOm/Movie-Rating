from rest_framework import serializers
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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


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
