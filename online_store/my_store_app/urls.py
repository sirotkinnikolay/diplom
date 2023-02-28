from django.contrib import admin
from django.urls import include, path
from my_store_app.views import *

urlpatterns = [
    path('', CategoryView.as_view(), name='index'),
    path('register/', register_view, name='register'),
    path('logout/', AuthorLogoutView.as_view(), name='logout'),
    path('login/', Login.as_view(template_name='login.html'), name='login')

]
