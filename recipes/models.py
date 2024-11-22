from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    steps = models.TextField(verbose_name="Шаги приготовления")
    ingredients = models.TextField(verbose_name="Ингредиенты")  # New field for ingredients
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления (в минутах)")
    image = models.ImageField(upload_to='recipes/images/', verbose_name="Изображение", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="recipes")
    categories = models.ManyToManyField('Category', verbose_name="Категории", related_name="recipes", through='RecipeCategory')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории", null=True, blank=True)

    def __str__(self):
        return self.name

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт", related_name="recipe_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="recipe_categories")
    is_primary = models.BooleanField(default=False, verbose_name="Основная категория")

    class Meta:
        unique_together = ('recipe', 'category')

    def __str__(self):
        return f"{self.recipe.title} - {self.category.name}"



