from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Product(models.Model):
    CATEGORY = [
        ('Мебел', 'Мебел'),
        ('Накит', 'Накит'),
        ('Часовници', 'Часовници'),
        ('Кујнски прибор', 'Кујнски прибор'),
        ('Декоративни работи', 'Декоративни работи'),
        ('Интериор', 'Интериор'),
        ('Музички инструменти', 'Музички инструменти'),
        ('Играчки', 'Играчки'),
        ('Текстил', 'Текстил'),
    ]

    # Info about the the product seller
    seller_name_and_surname = models.CharField(max_length=100, null=True, blank=True)
    seller_city = models.CharField(max_length=100, null=True, blank=True)
    seller_email = models.CharField(max_length=100, null=True, blank=True)
    seller_phone_number = models.CharField(max_length=100, null=True, blank=True)

    # Info about the product
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)
    category = models.CharField(max_length=255, null=False, blank=False, choices=CATEGORY)
    model = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to="The_Antiquarians_app/static/images/images")
    description = models.TextField(max_length=500)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return f"{self.name} - {self.model} - {self.category}"


class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)

    @property
    def get_shopping_cart_total_price(self):
        order_items = self.orderitem_set.all()
        total_price = sum([item.get_shopping_cart_item_price for item in order_items])
        return total_price


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False, blank=False)

    def get_shopping_cart_item_price(self):
        total_price = self.product.price * self.quantity
        return total_price

    # def __str__(self):
    #     return f"{self.product.name} - {self.quantity}"


class Delivery(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=False)

    name = models.CharField(max_length=50, null=False, blank=False)
    surname = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField()
    phone_number = models.IntegerField(null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    postal_code = models.IntegerField(null=False, blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)

    card_payment = models.BooleanField(default=False)
    card_name_surname = models.CharField(max_length=100)
    card_number = models.IntegerField()
    card_valid_until = models.CharField(max_length=5)
    card_ccv = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.surname} - {self.order}"
