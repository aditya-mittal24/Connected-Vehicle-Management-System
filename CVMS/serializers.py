from rest_framework import serializers
from .models import Vehicle, Trip, Owner, Maintenance, Sensor


class VehicleDistanceSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name')
    total_distance_traveled = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Vehicle
        fields = ["vehicle_id", "make", "model", "owner_name", "total_distance_traveled"]
        
class CustomVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["vehicle_id", "make", "model"]
        
class MaintenanceHistorySerializer(serializers.ModelSerializer):
    vehicle = CustomVehicleSerializer()
    class Meta:
        model = Maintenance
        fields = "__all__"
        
class SensorAnomaliesSerializer(serializers.ModelSerializer):
    vehicle = CustomVehicleSerializer()
    class Meta:
        model = Sensor
        fields = ["vehicle", "sensor_type", "sensor_reading", "timestamp"]
        
class FrequentTripsSerializer(serializers.ModelSerializer):
    number_of_trips = serializers.IntegerField()
    class Meta:
        model = Vehicle
        fields = ["vehicle_id", "make", "model", "number_of_trips"]

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"
        
        
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"
        
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
        
class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"
        
