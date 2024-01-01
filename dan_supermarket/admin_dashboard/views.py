from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    return render(request, 'admin_dashboard/index.html')

def add_product(request):
    return render(request, 'admin_dashboard/add_product.html')