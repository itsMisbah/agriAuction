from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from crops.models import Crop
from .forms import CropForm

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
            return redirect('home')   
    else:
        form = CropForm()

    return render(request, 'crops/add_crop.html', {'form': form})

@login_required
def crop_list(request):
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
    crop = Crop.objects.get(id=crop_id)
    return render(request, 'crops/crop_detail.html', {'crop': crop})

@login_required
def edit_crop(request, crop_id):
    crop = Crop.objects.get(id=crop_id)
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

def crop_bid(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    return render(request, 'crops/crop_bid.html', {'crop': crop})