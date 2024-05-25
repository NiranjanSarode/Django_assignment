from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SalesRecord
from .forms import SalesRecordForm

@csrf_exempt
def index(request):
    if request.method == 'GET':
        records = list(SalesRecord.objects.all().values())
        return JsonResponse(records, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def add_record(request):
    if request.method == 'POST':
        form = SalesRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
