# ==================================
# ==================================
#  Import Core Dependencies 
# ==================================
# ==================================
from django.contrib.auth import logout
from django.shortcuts import redirect


# ==================================
# ==================================
#  Logout handler
# ==================================
# ==================================
def logout_view(request):

    # Default Django Logout, It Removes Session ID and Remove Session
    logout(request)

    # Redirect To Login Page After Logout 
    return redirect('login')
