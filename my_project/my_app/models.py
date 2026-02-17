from django.db import models
from django.utils import timezone
from datetime import timedelta

class Purchase(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(default=timezone.now)
    return_deadline = models.DateTimeField()
    status = models.CharField(
        max_length=50, 
        choices=[
            ('Delivered', 'Delivered'),
            ('Returned', 'Returned'),
            ('Return Requested', 'Return Requested'),
            ('Pending Approval', 'Pending Approval'),
            ('Refund Processed', 'Refund Processed'),
            ('Return Rejected', 'Return Rejected')
        ],
        default='Delivered'
    )

    def save(self, *args, **kwargs):
        if not self.return_deadline:
            self.return_deadline = timezone.now() + timedelta(days=15)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} - {self.purchase_date.strftime('%Y-%m-%d')}"

