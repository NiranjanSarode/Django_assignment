from django import forms
from .models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale  
        fields = ['date', 'product', 'amount', 'region', 'receipt_photo']  # Include all fields
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Make it a date picker
        }

