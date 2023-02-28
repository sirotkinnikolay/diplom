from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.models import User


# ====================регистрация и аутентификация =====================================================================


def register_view(request):  # +
    """Функция регистрации нового пользователя"""

    if request.method == 'POST':
        form = AuthorRegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('login')
            user = User.objects.create_user(username=username, first_name=full_name, email=email)
            user.set_password(raw_password)
            user.save()
            login(request, user)
            Profile.objects.create(user=user, username=username, full_name=full_name, phone=phone, email=email)
        return redirect('/')

    return render(request, 'registr.html')


class AuthorLogoutView(LogoutView):  # +
    """Выход из учетной записи"""
    next_page = '/'


class Login(LoginView):
    """Вход в учетную запись"""
    def form_valid(self, form):
        return super().form_valid(form)

# ======================================================================================================================

class CategoryView(View):
    def get(self, request):
        category = CategoryProduct.objects.all()
        return render(request, 'index.html', {'categories': category})
