from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from crops.models import Bid, Crop
from .forms import CropForm
from decimal import Decimal

@login_required
def add_crop(request):
    if request.user.role != 'FARMER':
        messages.error(request, 'Only farmers can add crops.')
        return redirect('home') 

    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES) 
        if form.is_valid():
            crop = form.save(commit=False) 
            crop.farmer = request.user      
            crop.save()                    
            messages.success(request, 'Crop added successfully!')
            return redirect('crop_detail', crop_id=crop.id)   
    else:
        form = CropForm()

    return render(request, 'crops/add_crop.html', {'form': form})

@login_required
def crop_list(request):
    if request.user.role != 'FARMER':
        messages.error(request, 'Only farmers can view their listings.')
        return redirect('home')
    
    crops = Crop.objects.filter(farmer=request.user) 
    category = request.GET.get('category')
    status = request.GET.get('status')
    if category:
        crops = crops.filter(category=category)
    if status:
        crops = crops.filter(status=status)
    return render(request, 'crops/my_listings.html', {'crops': crops})

@login_required
def crop_detail(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if request.user != crop.farmer:
        messages.error(request, 'You are not authorized to view this crop.')
        return redirect('home')
    return render(request, 'crops/crop_detail.html', {'crop': crop})

@login_required
def edit_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if request.user != crop.farmer:
        messages.error(request, 'You are not authorized to edit this crop.')
        return redirect('home')

    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop updated successfully!')
            return redirect('crop_detail', crop_id=crop.id)
    else:
        form = CropForm(instance=crop)

    return render(request, 'crops/edit_crop.html', {'form': form, 'crop': crop})

@login_required
def marketplace(request):
    if request.user.role != 'BUYER':
        messages.error(request, 'Only buyers can access the marketplace.')
        return redirect('home')

    crops = Crop.objects.filter(status='active')
    category = request.GET.get('category')
    search = request.GET.get('search')
    if category:
        crops = crops.filter(category=category)
    if search:
        crops = crops.filter(title__icontains=search)
    return render(request, 'crops/marketplace.html', {'crops': crops})

@login_required
def crop_bid(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    highest_bid = crop.bids.order_by('-bid_amount').first()
    current_highest_bid = highest_bid.bid_amount if highest_bid else crop.base_price
    if request.user == crop.farmer:
        messages.error(request, 'You cannot place bid at your own crop.')
        return redirect('home')
    
    if crop.status != 'active':
        messages.error(request, 'Cannot bid on inactive crop.')
        return redirect('marketplace')
    
    if request.method == 'POST':
        current_bid_amount = request.POST.get('bid_amount')
        if not current_bid_amount:
            messages.error(request, 'Please enter a bid amount.')
            return redirect('crop_bid', crop_id=crop.id)
        
        if Decimal(current_bid_amount) > current_highest_bid:
            bid = Bid(crop=crop, bidder=request.user, bid_amount=current_bid_amount)
            bid.save()
            messages.success(request, 'Your bid has been placed successfully!')
            return redirect('crop_bid', crop_id=crop.id)
        else:
            messages.error(request, 'Your bid must be higher than the current bid and the base price.')
            return redirect('crop_bid', crop_id=crop.id)
    bids = crop.bids.order_by('-bid_amount')
    return render(request, 'crops/crop_bid.html', {'crop': crop, 'bids': bids})