from .models import Vehicle, Trip
from django.db.models import Count, Q
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class VehicleDistanceView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, *args, **kwargs):
        # Calculate the date 30 days ago from today
        thirty_days_ago = timezone.now() - timedelta(days=30)

        vehicles = Vehicle.objects.all()

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
        speed_anomalies = Sensor.objects.filter(
            sensor_type='Speed', sensor_reading__gt=120)
        fuel_anomalies = Sensor.objects.filter(
            sensor_type='Fuel Level', sensor_reading__lt=10)

        # combining both anomaly sets
        anomalies = speed_anomalies | fuel_anomalies

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
        
        print(frequent_trip_vehicles)

        serializer = FrequentTripsSerializer(frequent_trip_vehicles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VehiclesView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        vehicles = Vehicle.objects.all()
        make = request.query_params.get('make')
        if make: 
            vehicles = vehicles.filter(make=make)
        serializer = VehicleSerializer(vehicles, many=True)

        return Response(serializer.data)

    def post(self, request):
        serialized_item = VehicleSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
 
class OwnersView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        owners = Owner.objects.all()
        serializer = OwnerSerializer(owners, many=True) 
        return Response(serializer.data)

    def post(self, request):
        serialized_item = OwnerSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)


class SingleVehiclesView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)


class TripView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serialized_item = TripSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)


class SensorView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        sensors = Sensor.objects.all()
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serialized_item = SensorSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)


class MaintenanceView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        maintenance_records = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenance_records, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serialized_item = MaintenanceSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
