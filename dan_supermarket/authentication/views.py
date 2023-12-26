from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
import json

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username is already in use, please choose another.'}, status=409)
        return JsonResponse({'username_valid' : True})
    
class EmailValidationView(View):
     def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Invalid email. Please try again.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email is already taken. Please choose another email'}, status=409)
        return JsonResponse({'email_valid' : True})
    


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
