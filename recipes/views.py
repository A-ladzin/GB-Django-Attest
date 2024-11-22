from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Recipe, Category
from .forms import RecipeForm, CustomUserCreationForm
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

import random



class HomeView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    queryset = Recipe.objects.order_by('?')[:5]  # 5 случайных рецептов

@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def is_admin(user):
    return user.is_staff

def get_syrniki(request):
    return render(request, 'hello/Sem_2_HW_recipe.html')


@user_passes_test(is_admin)
@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()  # Сохранение ManyToMany связей
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})


@user_passes_test(is_admin)
@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Check if the user is the author or has staff privileges
    if request.user != recipe.author and not request.user.is_staff:
        return redirect('recipe_detail', pk=recipe.pk)  # Redirect if not authorized to edit

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)  # Handle POST data and files
        if form.is_valid():
            form.save()  # Save the changes to the recipe
            return redirect('recipe_detail', pk=recipe.pk)  # Redirect to the recipe detail page after saving
    else:
        form = RecipeForm(instance=recipe)  # If not POST, load the current recipe data into the form

    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})




def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизовать пользователя после регистрации
            return redirect('home')  # Перенаправить на главную страницу
    else:
        form = CustomUserCreationForm()  # Пустая форма для GET-запроса
    return render(request, 'registration/signup.html', {'form': form})


def home(request):
    recipes = Recipe.objects.all()
    random_recipes = random.sample(list(recipes), 5)  # Получить 5 случайных рецептов
    return render(request, 'home.html', {'recipes': random_recipes})

@login_required
def index(request):
    return redirect('home')



def check_user(request, username):
    try:
        user = User.objects.get(username=username)
        return JsonResponse({'exists': True})
    except User.DoesNotExist:
        return JsonResponse({'exists': False})
    
@csrf_exempt
def authenticate_user(request):
    # Получаем имя пользователя и пароль из запроса
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Проверка данных
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Если пользователь найден и пароль правильный
        login(request, user)  # Выполняем логин пользователя
        return JsonResponse({'authenticated': True, 'message': 'Login successful!'})
    else:
        # Если пользователь не найден или пароль неправильный
        return JsonResponse({'authenticated': False, 'message': 'Invalid username or password'})
    

