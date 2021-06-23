from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
# Create your views here.

def home_view(request):
    return render(request, 'sales/home.html', {})

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDeatailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'

def sale_list_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/main.html', {'obkect_list': qs})

def sale_detail_view(request, pk):
    obj = Sale.objects.get(pk=pk)
    return render(request, 'sales/main.html', {'object': obj})