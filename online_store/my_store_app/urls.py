from django.contrib import admin
from django.urls import include, path
from my_store_app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', CategoryView.as_view(), name='index'),
    path('register/', register_view, name='register'),
    path('logout/', AuthorLogoutView.as_view(), name='logout'),
    path('login/', Login.as_view(template_name='login.html'), name='login'),
    path('product/<int:pk>/', ProductdView.as_view(), name='one_product'),
    path('account/<int:pk>/', AccountView.as_view(), name='account'),
    path('edit_profile/', AccountUpdateView.as_view(), name='edit_profile'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('about/', AboutView.as_view(), name='about'),
    path('sale/', SaleView.as_view(), name='sale'),
    path('user_office/<int:pk>/', UserOfficeView.as_view(), name='user_office'),
    path('cart/', CartView.as_view(), name='cart'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
