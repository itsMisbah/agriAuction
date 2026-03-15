from django.contrib import admin
from .models import Crop, Bid

# Register your models here.
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['title', 'farmer', 'category', 'status', 'start_date', 'end_date']
    search_fields = ['title', 'location']
    list_filter = ['category', 'status', 'quality_grade']
    fieldsets = (
        ('Crop Information', {
            'fields': ('title', 'description', 'base_price', 'category')
        }),
        ('Additional Details', {
            'fields': ('farmer', 'images', 'location', 'weight', 'quality_grade')
        }),
        ('Auction Details', {
            'fields': ('status', 'start_date', 'end_date'),
        }),
    )
    readonly_fields = ['start_date']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['crop', 'bidder', 'bid_amount', 'bid_time']
    search_fields = ['crop__title', 'bidder__username']
    list_filter = ['crop', 'bidder']
    fieldsets = (
        ('Bid Information', {
            'fields': ('crop', 'bidder', 'bid_amount')
        }),
        ('Bid Details', {
            'fields': ('bid_time',),
        }),
    )
    readonly_fields = ['bid_time']