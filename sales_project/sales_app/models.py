from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SalesRecord(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=100)
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=100)
    receipt_photo = models.ImageField(upload_to='receipts/')

    def __str__(self):
        return f"{self.product} sold in {self.region} on {self.date} for {self.sales_amount}"
