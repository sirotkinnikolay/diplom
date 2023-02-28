from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.models import User
import os


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
    """Формирование списка категорий, популярных товаров,
     лимитированных, баннеров и путей до изображений этих категорий (index.html)"""
    def get(self, request):
        category = CategoryProduct.objects.all()
        popular_product = Product.objects.all().order_by('-reviews')[:8]
        limited_offer = Product.objects.filter(limited_offer=True)[:1]
        try:
            discount_price = round(limited_offer[0].price/100 * (100 - limited_offer[0].discount))
        except ZeroDivisionError:
            discount_price = limited_offer[0].price
        banners = Product.objects.all().order_by('-rating')
        limited_edition = Product.objects.filter(limited_edition=True)[:4]

        return render(request, 'index.html', {'categories': category,
                                              'popular_product': popular_product,
                                              'limited_offer': limited_offer,
                                              'banners': banners,
                                              'limited_edition': limited_edition,
                                              'discount_price': discount_price})
