from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Movie, Genre, Person, Role, Country, Language

class RoleInline(admin.TabularInline):
    model = Role
    extra = 0

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'rating', 'votes')
    list_filter = ('year', 'genres', 'countries', 'languages')
    search_fields = ('title', 'genres__name', 'directors__name', 'writers__name', 'actors__name', 'countries__name', 'languages__name')
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

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Language, LanguageAdmin)
