from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from crops.models import Crop, Bid
from api.serializers import (
    CropSerializer,
    CropCreateAndUpdateSerializer,
    CropListSerializer,
    BidSerializer,
    BidCreateSerializer,
)


class CropViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CropCreateAndUpdateSerializer
        if self.action == 'list':
            return CropListSerializer
        return CropSerializer

    def get_queryset(self):
        user = self.request.user
        base_qs = Crop.objects.select_related('farmer', 'winner').prefetch_related('bids')
        if user.role == 'FARMER':
            return base_qs.filter(farmer=user)
        return base_qs.filter(status='active')

    def perform_create(self, serializer):
        if self.request.user.role != 'FARMER':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only farmers can list crops.")
        serializer.save(farmer=self.request.user)

    def update(self, request, *args, **kwargs):
        crop = self.get_object()
        if crop.farmer != request.user:
            return Response({'error': 'You are not the owner of this crop.'}, status=status.HTTP_403_FORBIDDEN)
        if crop.status != 'active':
            return Response({'error': 'Only active crops can be updated.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     crop = self.get_object()
    #     if crop.farmer != request.user:
    #         return Response({'error': 'You are not the owner of this crop.'}, status=status.HTTP_403_FORBIDDEN)
    #     if crop.status == 'active' and crop.bids.exists():
    #         return Response({'error': 'Cannot delete a crop that already has bids.'}, status=status.HTTP_400_BAD_REQUEST)
    #     return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='place-bid')
    def place_bid(self, request, pk=None):
        if request.user.role != 'BUYER':
            return Response({'error': 'Only buyers can place bids.'}, status=status.HTTP_403_FORBIDDEN)
        crop = self.get_object()
        serializer = BidCreateSerializer(
            data=request.data,
            context={'crop': crop, 'request': request},
        )
        if serializer.is_valid():
            bid = serializer.save(bidder=request.user, crop=crop)
            return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='bids')
    def list_bids(self, request, pk=None):
        crop = self.get_object()
        if request.user.role == 'FARMER' and crop.farmer != request.user:
            return Response({'error': 'You are not the owner of this crop.'}, status=status.HTTP_403_FORBIDDEN)
        bids = crop.bids.select_related('bidder').order_by('-bid_amount')
        return Response(BidSerializer(bids, many=True).data)