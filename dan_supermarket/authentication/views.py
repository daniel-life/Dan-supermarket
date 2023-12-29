from django.shortcuts import render, redirect
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
    


# This is a Django class-based view for customer registration
class RegistrationView(View):
    # This method is called when a GET request is made to the view
    def get(self, request):
        # Render the registration page
        return render(request, 'authentication/register.html')

    # This method is called when a POST request is made to the view
    def post(self, request):
        # Retrieve the username, email, and password from the POST data
        username  = request.POST['username']
        email  = request.POST['email']
        password  = request.POST['password']

        # Store the POST data in a context dictionary
        context = {
            'fieldValues': request.POST
        }

        # Check if the username already exists
        if not User.objects.filter(username=username).exists():
            # Check if the email already exists
            if not User.objects.filter(email=email).exists():
                # Check if the password is less than 6 characters long
                if len(password) < 6:
                    # If it is, show an error message and re-render the registration page
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                
                # If the username and email do not exist and the password is long enough,
                # create a new customer and set their password
                customer = User.objects.create_user(username=username, email=email)
                customer.set_password(password)
                # Set the customer as inactive until they verify their email
                customer.is_active = False
                # Save the customer object to the database
                customer.save()

                # Get the current site domain
                current_site = get_current_site(request)
                # Create the email body with necessary information for email verification
                email_body = {
                    'customer': customer,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
                    'token': token_generator.make_token(customer),
                }

                # Create the activation link
                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                # Create the email subject
                email_subject = 'Activate your account'
                # Create the full activation URL
                activate_url = 'http://'+current_site.domain+link
               
                # Create the email message
                emailMessage = EmailMessage(
                    email_subject,
                    'Hi '+customer.username + ',\nPlease the link below to activate your account \n'+ activate_url,
                    'noreply@dansupermarket.com',
                    [email],
                )
                # Send the email
                emailMessage.send(fail_silently=False)
                # Show a success message
                messages.success(request, 'Account created. Check your email to verify email address')
                # Render the registration page
                return render(request, 'authentication/register.html')
            
        # If the username or email already exists, re-render the registration page
        return render(request, 'authentication/register.html')
        

class VerificationView(View):
      def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            customer = User.objects.get(pk=id)

            if not token_generator.check_token(customer, token):
                return redirect('login'+'?message='+'Customer already activated')
            if customer.is_active:
                return redirect('login')
            
            customer.is_active = True
            customer.save()
            messages.success(request, 'Account activated successfully')
            redirect('login')
        except Exception as e:
            pass

        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
              # Check if the customer exists
            try:
               customer = User.objects.get(username=username)
            
            except User.DoesNotExist:
                messages.error(request, 'Invalid credentials, try again')
                return render(request, 'authentication/login.html')
            
             # Check if the customer is active
            if not customer.is_active:
                messages.error(request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            

            # Authenticate the customer
            customer = auth.authenticate(username=username, password=password)
            if customer:
                auth.login(request, customer)
                messages.success(request, 'Welcome, ' + customer.get_username() + ' you are now logged in')
                return redirect('admin_dashboard')

            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')
    

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'you have been logged out')
        return redirect('login')
