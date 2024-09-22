from django.urls import path
from .views import *

urlpatterns = [
    path('', VehiclesView.as_view(), name='vehicle-list'),  # lists all vehicles
    path('<int:pk>/', SingleVehiclesView.as_view(), name='single-vehicle'),  # lists single vehicle
    path('owners/', OwnersView.as_view(), name='owner-list'),  # lists all owners
    path('trips/', TripView.as_view(), name='trip-list'),  # lists all trips
    path('sensors/', SensorView.as_view(), name='sensor-list'),  # lists all sensors
    path('maintenance_history/', MaintenanceView.as_view(), name='maintenance-records'),  # lists all maintenance records
    path('distance_traveled/', VehicleDistanceView.as_view(), name='vehicle-distance'),  # distance traveled by all the vehicles
    path('distance_traveled/<int:vehicle_id>', SingleVehicleDistanceView.as_view(), name='single-vehicle-distance'), #distance traveled by a single vehicle
    path('sensor_anomalies/', SensorAnomaliesView.as_view(), name='sensor-anomalies'), # sensor anomalies
    path('<int:pk>/maintenance_history', MaintenanceHistoryView.as_view(), name='maintenance-history'), # maintenancy history of a single vehicle
    path('frequent_trips/', FrequentTripsView.as_view(), name="frequent-trips") # trips > 5 in the last 7 days
]
