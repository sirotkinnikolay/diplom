from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView
from my_store_app.models import *
from my_store_app.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.models import User
from django.db.models import Count
import os
import datetime


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
    """Страница информации об одном товаре"""
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


class AccountView(DetailView):
    """Страница информации о пользователе"""
    model = Profile
    template_name = 'profile.html'


class UserOfficeView(DetailView):
    """Личный кабинет пользователя с заказами"""
    model = Profile
    template_name = 'account.html'


class AccountUpdateView(View):
    """Изменение данных пользователя через форму на странице profile.html"""

    def post(self, request):
        user = Profile.objects.get(id=request.user.id)
        user_auth = User.objects.get(id=request.user.id)
        user_auth.first_name = request.POST['name']
        user_auth.email = request.POST['mail']
        user.phone = request.POST['phone']
        user.full_name = request.POST['name']
        user.email = request.POST['mail']

        if request.POST['password'] == '' or request.POST['passwordReply'] == '':
            return redirect('/')

        if request.POST['password'] == request.POST['passwordReply']:
            user_auth.set_password(str(request.POST['password']))
        user.save()
        user_auth.save()
        return redirect('/')


class CatalogView(View):
    """Вывод каталога товаров и функция упорядочивания вывода, фильтрация"""

    def get(self, request):
        sort_flag = int(request.GET['q'])
        if sort_flag == 1:
            products = Product.objects.all().order_by('-reviews')
        elif sort_flag == 2:
            products = Product.objects.all().order_by('price')
        elif sort_flag == 3:
            products = Product.objects.all().order_by('-feedback')
            print('отзывы')
        elif sort_flag == 4:
            products = Product.objects.all().order_by('-date')
        else:
            products = Product.objects.all()
        tags_list = []
        for i in products:
            for n in i.tags.all():
                if n.tags_name not in tags_list:
                    tags_list.append(n.tags_name)
        return render(request, 'catalog.html', {'products': products, 'tags': tags_list})


class AboutView(View):
    """Страница информации о магазине"""

    def get(self, request):
        product_0 = Product.objects.all()[0]
        product_1 = Product.objects.all()[1]
        return render(request, 'about.html', {'product_0': product_0, 'product_1': product_1})


class SaleView(View):
    """Страница распродажи товаров"""

    def get(self, request):
        sal_products = Sales.objects.all()
        for limit in sal_products:
            if limit.dateTo <= datetime.datetime.now().date():
                Sales.objects.filter(id=limit.id).delete()
        return render(request, 'sale.html', {'sal_products': sal_products})


class CartView(View):
    def get(self, request):
        print(request.user.id)
        cart = Basket.objects.all()
        return render(request, 'cart.html', {'cart': cart})

