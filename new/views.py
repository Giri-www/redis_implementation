# from django.shortcuts import render

# # Create your views here.
# # views.py

# from django.core.cache import cache
# from django.shortcuts import render

# def expensive_view(request):
#     # Try to get the data from the cache
#     data = cache.get('expensive_data')
#     if not data:
#         # Data not in cache, so compute it
#         data = compute_expensive_data()
#         # Store data in the cache for 15 minutes
#         cache.set('expensive_data', data, timeout=60)
#     return render(request, 'template.html', {'data': data})

# def compute_expensive_data():
#     # Simulate an expensive computation
#     return "This is some expensive data"
# ================================================================

# views.py
# your_app/views.py

# from django.shortcuts import render
# from django.core.cache import cache
# import redis

# # Direct Redis connection
# r = redis.Redis(host='localhost', port=6379, db=0)

# def store_data(request):
#     cache.set('my_key', 'Hello from Django cache!', timeout=60)
#     r.set('direct_key', 'Hello from Redis-py!')
#     return render(request, 'store_data.html', {'message': 'Data stored successfully!'})

# def retrieve_data(request):
#     cache_value = cache.get('my_key')
#     direct_value = r.get('direct_key')
#     return render(request, 'retrieve_data.html', {
#         'cache_value': cache_value,
#         'direct_value': direct_value.decode('utf-8') if direct_value else 'No value found'
    # })

# ===============================================================USING FORM FIELD ===============================
from django.shortcuts import render, redirect
from django.core.cache import cache
import redis
from .forms import DataForm

# # Direct Redis connection
# r = redis.Redis(host='localhost', port=6379, db=0)

# def store_data(request):
#     if request.method == 'POST':
#         form = DataForm(request.POST)
#         if form.is_valid():
#             key = form.cleaned_data['key']
#             value = form.cleaned_data['value']
#             # Store data in Django cache
#             cache.set(key, value, timeout=60*15)
#             # Store data directly in Redis
#             r.set(key, value)
#             return redirect('store_data')
#     else:
#         form = DataForm()

#     return render(request, 'store_data.html', {'form': form})



# Direct Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

def store_data(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        value = request.POST.get('value')
        # Store data in Django cache
        cache.set(key, value, timeout=60)
        # Store data directly in Redis
        r.set(key, value)
        return redirect('store_data')
    else:
        form = DataForm()

    return render(request, 'store_data.html', {'form': form})

def retrieve_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            # Retrieve data from Django cache
            cache_value = cache.get(key)
            # Retrieve data from Redis
            direct_value = r.get(key)
            return render(request, 'retrieve_data.html', {
                'cache_value': cache_value,
                'direct_value': direct_value.decode('utf-8') if direct_value else 'No value found',
                'form': form
            })
    else:
        form = DataForm()

    return render(request, 'retrieve_data.html', {'form': form})
