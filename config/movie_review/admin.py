from django.contrib import admin
from .models import (
    Movie,
    Genre,
    Person,
    Role,
    Country,
    Language,
    Review,
    Profile,
)


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'rating', 'votes')
    list_filter = ('year', 'genres', 'countries', 'languages')
    search_fields = (
        'title',
        'genres__name',
        'directors__name',
        'writers__name',
        'actors__name',
        'countries__name',
        'languages__name',
    )
    inlines = [RoleInline]


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('movie', 'actor', 'character')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'value')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Review, ReviewAdmin)
