from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    file = models.FileField(upload_to='uploads', default='uploads/NoImageFound.png')
    total_sales_amount = models.IntegerField(default=0)
    total_sales = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    strip_session_id = models.CharField(max_length=512, unique=True)
    has_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.amount}"
