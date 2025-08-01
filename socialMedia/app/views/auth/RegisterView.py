# ==================================
# ==================================
#  Import Core Dependencies 
# ==================================
# ==================================
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login
from django.shortcuts import redirect, render


# ==================================
# ==================================
#  User Registeration Handler
# ==================================
# ==================================
def RegisterView(request):

   # Verify User Request Method (POST Alowed TO Register)
   if request.method=='POST':

      # Collect Data in Encoded-Form Formate
      name = request.POST.get('name')
      email = request.POST.get('email')
      password = request.POST.get('password')

      # Check all Fields of POST Data 
      if (name,email,password): 
        
      #   Check if User already Exists in Database or Not. Return alert if Found.
        if User.objects.filter(username=email):
               return JsonResponse({'objective':'user already exists'}, status=403)
        
        else:
            #   Build New User for Deafult User model of Django
               query = User(username=email,first_name=name,email=email,password=password)  

               # Make hased password for New User
               query.set_password(password)
               query.save()

               # Login New User to create New Session of Just Created User
               login(request, query)

               # After session creation done, redirect to home
               return redirect('home')
        
      #   Error If POST Data is incomplete or invalid (E.g Missing email, Password or Address)
      else:  JsonResponse({'objective':'invalid creds'}, status=403)

      # Renders register HTML on Non-POST requests.
   else:
      return render(request, 'auth/register.html')


