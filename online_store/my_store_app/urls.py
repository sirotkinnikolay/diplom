from django.contrib import admin
from django.urls import include, path
from my_store_app.views import *

urlpatterns = [
    path('', CategoryView.as_view()),
    path('register/', register_view, name='register'),
    path('login/', AuthorLoginView.as_view(), name='login'),
    path('logout/', AuthorLogoutView.as_view(), name='logout'),

]
