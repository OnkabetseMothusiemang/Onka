from django.shortcuts import render

# Create your views here.
def index(request):
   return render(request, 'tracking/index.html') 

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
import jwt

# Mock database
vehicle_locations = {}

# Authentication decorator
def authenticate(view_func):
    def wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'message': 'Authorization token is required'}, status=401)
        try:
            decoded = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token has expired'}, status=403)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Invalid token'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapped_view

# Endpoint for sending GPS data
@csrf_exempt
@login_required
def send_gps(request, vehicle_id):
    if request.method == 'POST':
        data = request.POST
        vehicle_locations[vehicle_id] = {
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'timestamp': datetime.now().isoformat()
        }
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

# Endpoint for retrieving vehicle location data
@csrf_exempt
@login_required
def get_location(request, vehicle_id):
    if request.method == 'GET':
        location = vehicle_locations.get(vehicle_id)
        if not location:
            return JsonResponse({'message': 'Vehicle location not found'}, status=404)
        return JsonResponse(location)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vehicle, GPSData
from .serializers import VehicleSerializer, GPSDataSerializer

class VehicleListView(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

# Product-cart

from django.shortcuts import render, redirect
from .models import Product, Cart

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart.quantity += quantity
            cart.save()
    return redirect('view_cart')

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


