from django.shortcuts import render, redirect
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView

# ====================регистрация и аутентификация =====================================================================


def register_view(request):  # +
    """Функция регистрации нового пользователя"""

    if request.method == 'POST':
        print(request.POST)
        form = AuthorRegisterForm(request.POST)
        if form.is_valid():
            print('форма валидна')
            full_name = form.cleaned_data.get('full_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('login')
            print(username)
            print(raw_password)

            # AttributeError: 'AnonymousUser' object has no attribute '_meta'

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Profile.objects.create(username=username, full_name=full_name, phone=phone, user_id=user.id, email=email)
        return redirect('/')

    return render(request, 'registr.html')


class AuthorLogoutView(LogoutView):  # +
    """Выход из учетной записи"""
    next_page = '/'


class AuthorLoginView(LoginView):  # +
    """Вход в учетную запись"""
    template_name = 'login.html'


# ======================================================================================================================


class CategoryView(View):
    def get(self, request):
        category = CategoryProduct.objects.all()
        return render(request, 'index.html', {'categories': category})
