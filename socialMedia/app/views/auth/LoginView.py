# ==================================
# ==================================
#  Import Core Dependencies 
# ==================================
# ==================================

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login


# ======================================================================================================
# ======================================================================================================
#  Check User Creds Send Via POST and authenticate by Django Deafault authentication system.
# ======================================================================================================
# ======================================================================================================

def LoginView(request):
   if request.method=='POST':

    #   User Creds 
      email = request.POST.get('email')
      password = request.POST.get('password')

    #   If email and password sent by user is valid
      if (email,password):

        # Authenicate user by username, Email was saved as a username in Registeration. Thus Authenticating Accordingly.
        user = authenticate(username = email, password=password)
        if user != None:
           
        #    Django Default Login System To Create User Session
           login(request, user)
           return redirect('home')
        
        # If creds are not valid, (e.g Missing Email or Password in request) redirect to Login Page
        else:
           return redirect('login')
           
      else:  JsonResponse({'objective':'invalid creds'})

    # if Request is not POST, Redirect to Login Page 
   else:
      return render(request, 'auth/login.html')
   
