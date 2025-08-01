from django.views.decorators.csrf import csrf_exempt
import stripe
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import json
from ...models import Book, Order

# /////////////////////////////////////////////////////////////////////////Order Handlers///////////////////////////////////////////////////////////////////////



@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        amount = int(data['amount'])  # amount in paisa or cents (not rupees/dollars)
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',  # or 'pkr' if supported in your account
            automatic_payment_methods={'enabled': True},
        )
        return JsonResponse({'clientSecret': intent.client_secret})

def checkout(request):
    return render(request, 'checkout.html', {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })


@csrf_exempt
def save_order(request):
   if request.method=='POST':
      data = json.loads(request.body)
      product_id = data['product_id']
      product= Book.objects.get(id=product_id)
      user_id = request.user.id
      quantity = data['quantity']
      

      if (product_id, user_id, quantity):
          Order.objects.create(product_id=product_id, user_id=user_id, quantity=quantity, name=product.name, quotes =product.quotes,genre=product.genre,year=product.year,pages=product.pages,desc=product.desc,price=product.price,author=product.author)
          return JsonResponse({"objective":"order saved success", "success":True}, status=200)
      else: 
            return JsonResponse({"objective":'data not valid', 'success':False}, status=401)
   else:
      return JsonResponse({"objective":'Method not allowed', 'success':False}, status=405)
   
# get order list
@csrf_exempt
def get_orders(request):
  query = Order.objects.filter(user_id=request.user.id)
  if not query:
      return JsonResponse({'objective':"library is empty","success":False, "empty":True}, status=200)
  products = []
  for q in query:
       data = {
            "id": 1,
            "title": q.quotes,
            "author":q.author,
            "genre":q.genre,
            "year": q.year,
            "pages": q.pages,
            "description": q.desc,
            "dateAdded": q.date,
            "product_id":q.product_id
            
       }
       products.append(data)
  return JsonResponse(products, safe=False, status=200)
  


