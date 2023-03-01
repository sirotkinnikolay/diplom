# Generated by Django 4.1.7 on 2023-03-01 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import my_store_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50, verbose_name='название категории')),
                ('image', models.FileField(null=True, upload_to='static/')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0, verbose_name='номер счета')),
                ('name', models.TextField(default='не указан', max_length=30)),
                ('month', models.DateField(auto_now_add=True)),
                ('year', models.DateField(auto_now_add=True)),
                ('code', models.IntegerField(default=0, verbose_name='код оплаты')),
            ],
            options={
                'verbose_name': 'Оплата',
                'verbose_name_plural': 'Оплата',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, verbose_name='цена товара')),
                ('discount', models.IntegerField(default=0, verbose_name='скидка % ')),
                ('count', models.IntegerField(default=0, verbose_name='количество ')),
                ('date', models.DateField(auto_now_add=True)),
                ('title', models.TextField(max_length=50, verbose_name='название товара')),
                ('description', models.TextField(max_length=100, verbose_name='описание товара')),
                ('limited_offer', models.BooleanField(default=False)),
                ('limited_edition', models.BooleanField(default=False)),
                ('product_picture', models.ImageField(null=True, upload_to='static/')),
                ('rating', models.IntegerField(default=0, verbose_name='счетчик покупок товара')),
                ('reviews', models.IntegerField(default=0, verbose_name='счетчик просмотров  товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store_app.categoryproduct', verbose_name='категория товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, default='-------', max_length=50, null=True, verbose_name='username')),
                ('full_name', models.CharField(blank=True, default='не указано', max_length=50, verbose_name='ФИО пользователя')),
                ('phone', models.CharField(blank=True, default='Не указано', max_length=30, null=True, unique=True, verbose_name='номер телефона')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email пользователя')),
                ('avatar', models.ImageField(default='', null=True, upload_to='static/', validators=[my_store_app.models.Profile.validate_image])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.TextField(max_length=50, verbose_name='название магазина')),
            ],
            options={
                'verbose_name': 'магазин',
                'verbose_name_plural': 'магазины',
            },
        ),
        migrations.CreateModel(
            name='TagsFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags_name', models.TextField(max_length=50, verbose_name='тэг товара')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='Specifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, verbose_name='название')),
                ('value', models.TextField(max_length=50, verbose_name='значение')),
                ('specifications', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store_app.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'Спецификация',
                'verbose_name_plural': 'Спецификации',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='количество товара по скидке')),
                ('dateFrom', models.DateField()),
                ('dateTo', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store_app.product', verbose_name='товар')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store_app.shop', verbose_name='магазин')),
            ],
            options={
                'verbose_name': 'Распродажа',
                'verbose_name_plural': 'Распродажа',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, default='Не указано', max_length=100, verbose_name='текст отзыва')),
                ('create_at', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store_app.profile', verbose_name='пользователь')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_title_product_set', to='my_store_app.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store_app.shop', verbose_name='магазин товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='my_store_app.tagsfile'),
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('delivery_type', models.TextField(default='не указан', max_length=30, verbose_name='способ доставки')),
                ('payment_type', models.TextField(default='не указан', max_length=30, verbose_name='способ оплаты')),
                ('total_cost', models.IntegerField(default=0, verbose_name='общая стоимость заказа')),
                ('status', models.TextField(default='не указан', max_length=30, verbose_name='статус оплаты')),
                ('city', models.TextField(default='не указан', max_length=30, verbose_name='город доставки')),
                ('address', models.TextField(default='не указан', max_length=30, verbose_name='адрес доставки')),
                ('product_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store_app.product', verbose_name='товар')),
                ('user_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_store_app.profile', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'История покупок',
                'verbose_name_plural': 'Истории покупок',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='колличество  товаров в корзине')),
                ('price', models.IntegerField(default=0, verbose_name='общая стоимость  товаров в корзине')),
                ('date', models.DateField(auto_now_add=True)),
                ('free_delivery', models.BooleanField(default=False, verbose_name='наличие бесплатной доставки')),
                ('product_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_store_app.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='static/')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='my_store_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateField(auto_now_add=True)),
                ('product', models.ManyToManyField(related_name='product', to='my_store_app.product')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='my_store_app.profile')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
    ]
