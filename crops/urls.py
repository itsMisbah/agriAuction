from django.urls import path
from . import views

urlpatterns = [
    path('add-crop/', views.add_crop, name='add_crop'),
    path('crop-list/', views.crop_list, name='crop_list'),
    path('crop-detail/<int:crop_id>/', views.crop_detail, name='crop_detail'),
    path('edit-crop/<int:crop_id>/', views.edit_crop, name='edit_crop'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('crop-bid/<int:crop_id>/', views.crop_bid, name='crop_bid'),
    path('my-bids/', views.my_bids, name='my_bids'),
]