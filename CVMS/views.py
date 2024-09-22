from .models import Vehicle, Trip
from django.db.models import Count, Q
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta, datetime
from django.db import models
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.cache import cache


class VehicleDistanceView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, *args, **kwargs):
        # Calculate the date 30 days ago from today
        thirty_days_ago = timezone.now() - timedelta(days=30)

        if cache.get("vehicles"):
            print("from cache")
            vehicles = cache.get("vehicles")
        else:
            vehicles = Vehicle.objects.all()
            print("from db")
            cache.set("vehicles", vehicles)
            cache.expire_at("vehicles", datetime.now() + timedelta(hours=1))

        for vehicle in vehicles:

            total_distance = Trip.objects.filter(
                vehicle=vehicle,
                start_time__gte=thirty_days_ago
            ).aggregate(total=models.Sum('distance_traveled'))['total'] or 0

            vehicle.total_distance_traveled = total_distance

        serializer = VehicleDistanceSerializer(vehicles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleVehicleDistanceView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, vehicle_id):
        # Calculate the date 30 days ago from today
        thirty_days_ago = timezone.now() - timedelta(days=30)

        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

        # filter the trips in last 30 days, sum the distance_traveled
        total_distance = Trip.objects.filter(
            vehicle=vehicle,
            start_time__gte=thirty_days_ago
        ).aggregate(total=models.Sum('distance_traveled'))['total'] or 0  # if no trips in last 30 days then 0km

        vehicle.total_distance_traveled = total_distance

        serializer = VehicleDistanceSerializer(vehicle)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SensorAnomaliesView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        if cache.get("vehicle_anomalies"):
            anomalies = cache.get("vehicle_anomalies")
        else:
            if cache.get("vehicle_sensors"):
                sensors = cache.get("vehicle_sensors")
            else:
                sensors = Sensor.objects.all()
                cache.set("vehicle_sensors", sensors)
                cache.expire_at("vehicle_sensors", datetime.now() + timedelta(hours=1))
            speed_anomalies = sensors.filter(
                sensor_type='Speed', sensor_reading__gt=120)
            fuel_anomalies = Sensor.objects.filter(
                sensor_type='Fuel Level', sensor_reading__lt=10)

            # combining both anomaly sets
            anomalies = speed_anomalies | fuel_anomalies
            
            cache.set("vehicle_anomalies", anomalies)
            cache.expire_at("vehicle_anomalies", datetime.now() + timedelta(hours=1))

        serializer = SensorAnomaliesSerializer(anomalies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MaintenanceHistoryView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        maintenance_records = Maintenance.objects.filter(vehicle=vehicle)

        serializer = MaintenanceHistorySerializer(
            maintenance_records, many=True)

        return Response(serializer.data)


class FrequentTripsView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, *args, **kwargs):
        # calculating the date 7 days ago from today
        seven_days_ago = timezone.now() - timedelta(days=7)

        # filtering trips that has start time greater than 7 days ago and number_of_trips > 5
        frequent_trip_vehicles = Vehicle.objects.annotate(
            number_of_trips=Count('trip', filter=Q(
                trip__start_time__gte=seven_days_ago))
        ).filter(number_of_trips__gt=5)
        

        serializer = FrequentTripsSerializer(frequent_trip_vehicles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VehiclesView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        if cache.get("vehicles"):
            print("from cache")
            vehicles = cache.get("vehicles")
        else:
            vehicles = Vehicle.objects.all()
            print("from db")
            cache.set("vehicles", vehicles)
            cache.expire_at("vehicles", datetime.now() + timedelta(hours=1))
        make = request.query_params.get('make')
        if make: 
            vehicles = vehicles.filter(make=make)
        
        serializer = VehicleSerializer(vehicles, many=True)

        return Response(serializer.data)

    def post(self, request):
        serialized_item = VehicleSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        cache.expire("vehicles", 0)
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        id = request.query_params.get("id")
        if id:
            vehicle = get_object_or_404(Vehicle, pk=id)
            vehicle.delete()
            cache.delete_many(keys=cache.keys('*vehicle*'))
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
 
class OwnersView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        if cache.get("owners"):
            print("from cache")
            owners = cache.get("owners")
        else:
            owners = Owner.objects.all()
            print("from db")
            cache.set("owners", owners)
            cache.expire_at("owners", datetime.now() + timedelta(hours=1))
        serializer = OwnerSerializer(owners, many=True) 
        return Response(serializer.data)

    def post(self, request):
        serialized_item = OwnerSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        cache.delete("owners")
        # cache.delete_many(keys=cache.keys('*.vehicle.*'))
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        id = request.query_params.get("id")
        if id:
            owner = get_object_or_404(Owner, pk=id)
            owner.delete()
            cache.delete("owners")
            cache.delete_many(keys=cache.keys('*vehicle*'))
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SingleVehiclesView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)


class TripView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        if cache.get("vehicle_trips"):
            trips = cache.get("vehicle_trips")
        else:
            trips = Trip.objects.all()
            cache.set("vehicle_trips", trips)
            cache.expire_at("vehicle_trips", datetime.now() + timedelta(hours=1))
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serialized_item = TripSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        cache.delete("vehicle_trips")
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)


class SensorView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        if cache.get("vehicle_sensors"):
            sensors = cache.get("vehicle_sensors")
        else:
            sensors = Sensor.objects.all()
            print("from db")
            cache.set("vehicle_sensors", sensors)
            cache.expire_at("vehicle_sensors", datetime.now() + timedelta(hours=1))
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serialized_item = SensorSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        cache.delete("vehicle_sensors")
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)


class MaintenanceView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        if cache.get("vehicle_maintenance"):
            maintenance_records = cache.get("vehicle_maintenance")
        else:
            maintenance_records = Maintenance.objects.all()
            cache.set("vehicle_maintenance", maintenance_records)
            cache.expire_at("vehicle_maintenance", datetime.now() + timedelta(hours=1))
        serializer = MaintenanceSerializer(maintenance_records, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serialized_item = MaintenanceSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        cache.delete("vehicle_maintenance")
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
