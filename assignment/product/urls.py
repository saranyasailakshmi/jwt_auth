from django.urls import path
from .views import (
    ProductCreateAPIView,
    ProductListAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView
)

urlpatterns=[
    path('create/', ProductCreateAPIView.as_view(), name='create-product'),          
    path('products/', ProductListAPIView.as_view(), name='list-products'),             
    path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name='update-product'),  
    path('delete/<int:pk>/', ProductDeleteAPIView.as_view(), name='delete-product'),  

]
