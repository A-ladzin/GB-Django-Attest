from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('index/', views.index, name='index'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/syrniki/', views.get_syrniki, name='recipe_detail'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/edit/<int:pk>/', views.edit_recipe, name='edit_recipe'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/check_user/<str:username>/', views.check_user, name='check_user'),
    path('api/authenticate_user/', views.authenticate_user, name='authenticate_user'),
]
