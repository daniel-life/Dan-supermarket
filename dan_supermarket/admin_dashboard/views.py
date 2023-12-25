from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'admin_dashboard/index.html')

def add_item(request):
    return render(request, 'admin_dashboard/add_item.html')