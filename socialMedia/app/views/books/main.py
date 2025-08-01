from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from ...models import Book
from django.core.cache import cache
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import stripe
from django.conf import settings
from django.forms.models import model_to_dict
import random



stripe.api_key = settings.STRIPE_SECRET_KEY

 
# /////////////////////////////////////////////////////////////////////////Home///////////////////////////////////////////////////////////////////////
def home(request):
      quotes = cache.get('quote')
      page = Paginator(Book.objects.all(), 5)    
      page_count = request.GET.get('page', 1) 
      page_obj = page.get_page(page_count) 
  
      if not quotes:
          raw = page_obj 
          quotes = list(raw)
          cache.set('quote', quotes, timeout=1000) 
  
      quotes = cache.get('quote') 
      
      return render(request, 'books/index.html', {'page_obj': page_obj, 'total': str(len(quotes))})


# /////////////////////////////////////////////////////////////////////////Detail///////////////////////////////////////////////////////////////////////
def detail(request, id):
    cache_key = f'product_{id}'
    product = cache.get(cache_key)

    if not product:
        book = get_object_or_404(Book, id=id)
        product = model_to_dict(book)
        cache.set(cache_key, product, timeout=1200)

    return render(request, 'books/detail.html', {
        'product': product,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })

# /////////////////////////////////////////////////////////////////////////Search Book///////////////////////////////////////////////////////////////////////
@csrf_exempt
def search(request):
 if request.method =="POST":
     requested_data = json.loads(request.body)
     query = Book.objects.filter(
     Q(name__icontains=requested_data['query']) | Q(author__icontains=requested_data['query'])
)
     if query:
        results=[]
        for q in query:
          data = {
              'id':q.id,
              'name':q.name, 
              'author':q.author
          } 
          results.append(data)
        return JsonResponse(results, safe=False)      
     else:
        return JsonResponse({'message':'no results found'}, safe=False)      
                     
 else:    
     return render(request, 'books/detail.html')

# /////////////////////////////////////////////////////////////////////////Recommandations///////////////////////////////////////////////////////////////////////    



# /////////////////////////////////////////////////////////////////////////User Library///////////////////////////////////////////////////////////////////////    
def library(request):
    return render(request, 'books/library.html')

# add books  
@csrf_exempt
def add_books(request):
    try:
        titles = [
            "The Last Dawn", "Echoes of Silence", "Whispers in the Dark", "Fragments of Time",
            "The Forgotten Path", "Journey Beyond Stars", "Shadow and Light", "Tides of Fate",
            "Songs of the Earth", "Memoirs of the Broken"
        ]

        quotes = [
            "Not all those who wander are lost.",
            "Even the darkest night will end and the sun will rise.",
            "Hope is the thing with feathers that perches in the soul.",
            "Every moment is a fresh beginning.",
            "To live will be an awfully big adventure.",
            "The past beats inside me like a second heart.",
            "Time you enjoy wasting was not wasted.",
            "A reader lives a thousand lives before he dies.",
            "Courage is found in unlikely places.",
            "We are all stories in the end."
        ]

        authors = [
            "Harper West", "Daniel Rivers", "Eleanor Bright", "Liam Cross",
            "Sophia Blake", "Noah Reed", "Ava Sinclair", "Mason Hart",
            "Isla Monroe", "Leo Hayes"
        ]

        for _ in range(20):
            Book.objects.create(
                name=random.choice(titles),
                quotes=random.choice(quotes),
                genre=random.choice(['Fiction', 'Non-fiction', 'Sci-Fi', 'Fantasy', 'Biography', 'History', 'Romance']),
                year=random.randint(1950, 2024),
                pages=random.randint(120, 850),
                desc=f"A captivating tale of {random.choice(['hope', 'betrayal', 'love', 'courage', 'redemption'])}, spanning generations.",
                price=random.randint(700, 2500),
                author=random.choice(authors),
                views=random.randint(0, 5000)
            )

        return JsonResponse({'message': '20 books added successfully!'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
