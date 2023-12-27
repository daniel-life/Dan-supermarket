from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str,  DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from flask import redirect
from validate_email import validate_email
from .utils import token_generator
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

    def post(self, request):
        # GET USER DATA
        #VALIDATE
        # Create a user account
        username  = request.POST.get('username')
        email  = request.POST.get('email')
        password  = request.POST.get('password')

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path to view
                #- getting domain we are on
                # - retrieve url to verification
                # - encode uid
                # - token
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})


                email_subject = 'Activate your account'
                activate_url = 'http://'+current_site.domain+link
               
                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ',\nPlease the link below to activate your account \n'+ activate_url,
                    'noreply@dansupermarket.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account Successfully created!')
                return render(request, 'authentication/register.html')
            
        return render(request, 'authentication/register.html')
        

class VerificationView(View):
      def get(self, request, uidb64, token):
            return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')