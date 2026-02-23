from rest_framework import serializers
from .models import Passenger

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'name', 'phone_number', 'email', 'password', 'wallet_balance']
        extra_kwargs = {
            'password': {'write_only': True}
        }
