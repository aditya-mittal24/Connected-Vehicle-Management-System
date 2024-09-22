from django.db import models

# Owner model
class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255) 
    contact_info = models.CharField(max_length=255) 

    def __str__(self):
        return self.name


# Vehicle model
class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True) 
    make = models.CharField(max_length=255) 
    model = models.CharField(max_length=255) 
    year = models.IntegerField() 
    fuel_type = models.CharField(max_length=50) 
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.vehicle_id} {self.make} {self.model} ({self.year})"


# Trip model
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True) 
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    start_time = models.DateTimeField()  
    end_time = models.DateTimeField()  
    start_location = models.CharField(max_length=255) 
    end_location = models.CharField(max_length=255)  
    distance_traveled = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.vehicle.make} {self.vehicle.model} on {self.start_time.date()}"
    
# Sensor model
class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    sensor_type = models.CharField(max_length=100)
    sensor_reading = models.DecimalField(max_digits=10, decimal_places=2) 
    timestamp = models.DateTimeField() 

    def __str__(self):
        return f"Sensor - {self.sensor_type} : {self.sensor_reading}"


# Maintenance model 
class Maintenance(models.Model):
    maintenance_id = models.AutoField(primary_key=True) 
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) 
    maintenance_type = models.CharField(max_length=255) 
    maintenance_date = models.DateField() 
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"Maintenance - {self.maintenance_type} on {self.maintenance_date}"


