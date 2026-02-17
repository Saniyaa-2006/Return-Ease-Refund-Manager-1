from django.contrib import admin
from .models import Purchase

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'purchase_date', 'return_deadline')
    list_filter = ('purchase_date',)
    search_fields = ('product_name',)
