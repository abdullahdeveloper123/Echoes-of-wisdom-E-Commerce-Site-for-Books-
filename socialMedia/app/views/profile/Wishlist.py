
# ==================================
# ==================================
#  Import Core Dependencies 
# ==================================
# ==================================
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json
from django.contrib.auth.decorators import login_required

# Import Custom Build Models
from ...models import Wishlist, Book


# ==================================
# ==================================
#  Wishlist Item Save Handler 
# ==================================
# ==================================
@csrf_exempt
def save(request):

    # Check request Method (POST needed with Book ID to save)
    if request.method == 'POST':

        # Check if User is Valid and Authenticated. Break Function If Not Verified.
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'status': 401})

        try:

            # Try to Load Json Body Sent By Client (This only takes JSON Formatted Data)
            data = json.loads(request.body)

            # Built-In Check If Product Exists in Database With Requested Product ID
            book = get_object_or_404(Book, id=data['id'])

        # If Got Error While Getting, Parsing, Fetching Product, This will Break Function on 400 Status Code.
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'success': False, 'status': 400, 'message': 'Invalid data'})

        # Check if Requested Product Is Already In User's WishList. If exists, It prevent Double Adds.
        if not Wishlist.objects.filter(product_id=book.id, user_id=request.user.id).exists():

            # Creating and Saving a New Wishlist Item in DB
            Wishlist.objects.create(
                product_id=book.id,
                name=book.name,
                quotes=book.quotes,
                desc=book.desc,
                price=book.price,
                author=book.author, 
                user_id=request.user.id,
                genre= book.genre
            )


        # Finally returning 200 As Successfully Saved Product in Wishlist
        return JsonResponse({'status': True, 'message': 'Book saved to wishlist'})
    
    # In-Case If Request Method Wasn't POST, This send 405 Status as BAD REQUEST
    return JsonResponse({'message': 'Method not allowed'}, status=405)


# Check User authentication and move to request if user is valid
@login_required(login_url='login')
def wishlist(request):
   
#    FIlter All Wishlist Items By User ID of Current User
   query = Wishlist.objects.filter(user_id=request.user.id)  

   return render(request, 'books/wishlist.html', {'query':query})

# Remove Item From Wishlist Handler, 
@csrf_exempt
def remove_wishlist(request):
    try:  
        data = json.loads(request.body)
        id = data['id']
        query = Wishlist.objects.get(id=id) 
        query.delete()
        return JsonResponse({"objective": 'successfully removed liked item'}, status=200)
    except Exception as e:
        return JsonResponse({"objective": str(e)}, status=400)  
