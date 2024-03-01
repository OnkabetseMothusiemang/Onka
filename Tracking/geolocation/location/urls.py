from django.urls import path
from .import views
from .views import VehicleListView

urlpatterns =[
    path('', views.index, name='index'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
]





