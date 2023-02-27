from django.contrib import admin
from django.urls import include, path
from my_store_app.views import *

urlpatterns = [
    path('index/', CategoryView.as_view()),
]