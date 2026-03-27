from rest_framework import serializers
from django.utils import timezone
from api.serializers.user_serializers import UserSerializer
from crops.models import Crop, Bid


class CropSerializer(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    is_ending_soon = serializers.SerializerMethodField()
    highest_bid = serializers.SerializerMethodField()
    highest_bidder = serializers.SerializerMethodField()

    class Meta:
        model = Crop
        fields = [
            'id', 'farmer', 'title', 'description', 'images',
            'location', 'weight', 'base_price', 'status',
            'category', 'start_date', 'end_date',
            'quality_grade', 'winner',
            'is_ending_soon', 'highest_bid', 'highest_bidder',
        ]
        read_only_fields = ['id', 'farmer', 'winner', 'start_date']

    def get_is_ending_soon(self, obj):
        return obj.is_ending_soon

    def get_highest_bid(self, obj):
        return obj.highest_bid

    def get_highest_bidder(self, obj):
        bidder = obj.highest_bidder
        return UserSerializer(bidder).data if bidder else None


class CropCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = [
            'title', 'description', 'location',
            'weight', 'base_price', 'category', 'end_date', 'quality_grade',
        ]

    def validate_end_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("End date must be in the future.")
        return value


class CropListSerializer(serializers.ModelSerializer):
    is_ending_soon = serializers.SerializerMethodField()
    highest_bid = serializers.SerializerMethodField()

    class Meta:
        model = Crop
        fields = [
            'id', 'title', 'images', 'location',
            'base_price', 'status', 'end_date',
            'highest_bid', 'is_ending_soon',
        ]

    def get_is_ending_soon(self, obj):
        return obj.is_ending_soon

    def get_highest_bid(self, obj):
        return obj.highest_bid


class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'crop', 'bidder', 'bid_amount', 'bid_time']
        read_only_fields = ['id', 'bidder', 'bid_time']


class BidCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['bid_amount']

    def validate(self, data):
        crop = self.context.get('crop')
        if not crop:
            raise serializers.ValidationError("Crop not found.")
        if crop.status != 'active':
            raise serializers.ValidationError("Bidding is closed for this crop.")
        highest = crop.highest_bid
        if highest is not None and data['bid_amount'] <= highest:
            raise serializers.ValidationError(
                f"Bid must be higher than current highest bid of {highest}."
            )
        return data