from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_id = models.CharField(max_length=100)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bill_number = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.product_name} - {self.customer.name}"

class ReturnRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    )
    
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    return_date = models.DateField()
    reason = models.TextField()
    bill_image = models.ImageField(upload_to='bills/', null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"Return: {self.purchase.product_name} by {self.purchase.customer.name}"
