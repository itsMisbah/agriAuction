from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Crop(models.Model):
    class crop_status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        SOLD = 'sold', 'Sold'
        EXPIRED = 'expired', 'Expired'

    class category(models.TextChoices):
        FRUITS = 'fruits', 'Fruits'                
        VEGETABLES = 'vegetables', 'Vegetables'    
        GRAINS = 'grains', 'Grains & Cereals'      
        LEGUMES = 'legumes', 'Pulses & Legumes'    
        NUTS_DRYFRUITS = 'nuts_dryfruits', 'Nuts & Dry Fruits' 
        OILSEEDS = 'oilseeds', 'Oilseeds'          
        SPICES = 'spices', 'Spices & Herbs'        
        OTHER = 'other', 'Other'

    class quality_grade(models.TextChoices):
        EXELLENT = 'exellent', 'Exellent'
        GOOD = 'good', 'Good'
        AVERAGE = 'average', 'Average'

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer')
    title = models.CharField(max_length=100)
    description = models.TextField()
    images = models.ImageField(upload_to='crop_images/', blank=True, null=True)
    location = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=crop_status.choices, default=crop_status.ACTIVE)
    category = models.CharField(max_length=20, choices=category.choices, default=category.OTHER)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    quality_grade = models.CharField(max_length=10, choices=quality_grade.choices, default=quality_grade.AVERAGE)

    def __str__(self):
        return self.title

    @property
    def is_ending_soon(self):
        return self.end_date <= timezone.now() + timedelta(hours=24)
    
class Bid(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - {self.bid_amount}"