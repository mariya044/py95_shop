from django.db import models

from users.models import CustomUser


class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="categories"


class Seller(models.Model):
    name=models.CharField(max_length=100)
    description = models.TextField()
    contact=models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Discount(models.Model):
    name=models.CharField(max_length=100)
    percent=models.PositiveIntegerField()
    date_start = models.DateField()
    date_end=models.DateField()
    def __str__(self):
        return f"{self.name}{self.percent}"


class Promocode(models.Model):
    name = models.CharField(max_length=100)
    percent = models.PositiveIntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    is_cumultaive =models.BooleanField()

    def __str__(self):
        return f"{self.name}{self.percent}"


class Product(models.Model):
    name=models.CharField(max_length=100)
    article=models.CharField(max_length=100)
    description=models.TextField()
    count_on_stock=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)

    discount=models.ForeignKey(Discount,null=True,blank=True, on_delete=models.SET_NULL)
    category=models.ForeignKey(Category,null=True,blank=True, on_delete=models.SET_NULL)
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}{self.article}"



class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="product_images/")

    def __str__(self):
        return  f"Image for{self.product}"

class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    count=models.PositiveIntegerField()


class Order(models.Model):
    STATUSES={
        ("IN PROCESS", "IN PROCESS"),
        ("PACKED","PACKED"),
        ("ON THE WAY","ON THE WAY "),
        ("DELIVERED","DELIVERED"),
        ("REFUSE","REFUSE")
    }
    DELIVERY_METHODS={
        ("COURIER","COURIER"),
        ("Post","Post"),
        ("SELF-DELIVERY","SELF-DELIVERY")
    }
    PAYMENT_METHODS={
        ("CASH","CASH"),
        ("CARD ONLINE","CARD ONLINE"),
        ("CARD OFFLINE","CARD OFFLINE")
    }
    PAYMENT_STATUS={
        ("PAID","PAID"),
        ("IN PROCESS","IN PROCESS"),
        ("CANCELED ","CANCELED")
    }
    NOTIF_TIMES={
        (24,24),
        (6,6),
        (1,1)

    }
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUSES)
    delivery_address = models.CharField(max_length=250, null=True, blank=True)
    delivery_methods = models.CharField(max_length=100, choices=DELIVERY_METHODS)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default="IN PROCESS")
    delivery_notification_before = models.PositiveIntegerField(choices=NOTIF_TIMES, default=6)

    def __str__(self):
        return f"{self.pk}{self.user.email}"


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()


class CashBack(models.Model):
    percent = models.IntegerField()
    treshold = models.PositiveIntegerField()

    def __str__(self):
        return str(self.percent)
