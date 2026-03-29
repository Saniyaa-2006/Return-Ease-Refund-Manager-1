from django import forms
from django.contrib.auth.models import User
from .models import Purchase, ReturnRequest, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone']
        
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product_name', 'product_id', 'purchase_date', 'price', 'bill_number']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['return_date', 'reason', 'bill_image']
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
