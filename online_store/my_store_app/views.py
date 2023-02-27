from django.shortcuts import render
from django.views import View
from my_store_app.models import *


class CategoryView(View):
    def get(self, request):
        category = CategoryProduct.objects.all()
        return render(request, 'index.html', {'categories': category})


