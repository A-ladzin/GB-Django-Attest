from django import forms
from .models import Recipe
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description',  'ingredients', 'steps', 'cooking_time', 'image', 'categories']  # Add ingredients here

        widgets = {
            'categories': forms.CheckboxSelectMultiple(),  # Example of how you might handle many-to-many fields
        }




class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
        label='Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}),
        label='Подтверждение пароля'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
