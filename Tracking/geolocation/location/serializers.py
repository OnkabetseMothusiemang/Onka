# serializers.py
from rest_framework import serializers
from .models import Vehicle, GPSData

class GPSDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSData
        fields = ['latitude', 'longitude', 'timestamp']

class VehicleSerializer(serializers.ModelSerializer):
    last_known_location = GPSDataSerializer(source='gps_data.last', read_only=True)

    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'model', 'manufacturer', 'year', 'last_known_location']
