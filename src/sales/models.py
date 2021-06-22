from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.utils.translation import activate

from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from sales.utils import generate_code
from .utils import generate_code

# Create your models here.

class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.price = self.product * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"

class Sale(models.Model):
    transaction_id = models.CharField(max_length=120, blank=True)
    positins = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sales for the amount of ${self.total_price}"

    def save(self, *args, **kwargs):

        if self.transaction_id == "":
            self.transaction_id = generate_code()
        
        if self.created in None:
            self.created = timezone.now()
        
        return super().save(*args, **kwargs)

    def get_position(self):
        return self.positins.all()

class CSV(models.Model):
    file_name = models.FileField(upload_to='csvs')
    activated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)