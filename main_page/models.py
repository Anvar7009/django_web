from django.db import models

# Create your models here.
#создать таблицу категории
class Category(models.Model):
    objects = models.Model
    #создать колонки для таблицы
    category_name = models.CharField(max_length=75)
    reg_date = models.DateTimeField(auto_now_add=True)

    # вывод информации в нормальном виде
    def __str__(self):
        return self.category_name

#создать таблицу для продуктов
class Product(models.Model):
    objects = models.Model
    #создаем колонки для таблицы продуктов
    product_name = models.CharField(max_length=125)
    product_count = models.IntegerField()
    product_price = models.FloatField()
    product_photo = models.ImageField(upload_to='media')
    product_des = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    reg_date = models.DateTimeField(auto_now_add=True)

    #вывод в нормальном виде
    def __str__(self):
        return self.product_name

#создать таблицу для корзины
class Cart(models.Model):
    #создаем колонки для таблицы корзины
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_product_quantity = models.PositiveSmallIntegerField(default=1)
    total_for_product = models.FloatField()

    reg_date = models.DateTimeField(auto_now_add=True)

    #вывод в нормальном виде
    def __str__(self):
        return str(self.user_product)


