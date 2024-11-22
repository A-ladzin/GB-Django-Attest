from django.contrib import admin
from .models import Recipe, Category, RecipeCategory

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cooking_time', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('categories', 'author')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'category', 'is_primary')
    list_filter = ('is_primary',)