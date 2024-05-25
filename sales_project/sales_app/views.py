from django.shortcuts import render, redirect
from .forms import SaleForm
from .models import Sale
from django.contrib import messages

def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST, request.FILES)  # Include FILES for photo upload
        if form.is_valid():
            form.save()
            messages.success(request, 'Sale data saved successfully!')
            return redirect('create_sale')  # Redirect to the same page to clear the form
    else:
        form = SaleForm()
    return render(request, 'sales_app/sale_form.html', {'form': form})
