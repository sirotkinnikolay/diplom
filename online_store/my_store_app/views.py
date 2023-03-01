from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
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
            discount_price = round(limited_offer[0].price / 100 * (100 - limited_offer[0].discount))
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


class ProductdView(DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductdView, self).get_context_data(**kwargs)
        tags_list = []
        picture_list = Files.objects.filter(product_id=self.kwargs['pk'])[:3]
        specification_list = Specifications.objects.filter(specifications_id=self.kwargs['pk'])

        for i in Product.objects.filter(id=self.kwargs['pk']):
            for n in i.tags.all():
                tags_list.append(n.tags_name)
        context['tags'] = tags_list
        context['files'] = picture_list
        context['specif'] = specification_list
        return context
