from django.contrib import admin
from .models import Owner, Vehicle, Maintenance, Sensor, Trip

# Register your models here.
admin.site.register(Owner)
admin.site.register(Vehicle)
admin.site.register(Maintenance)
admin.site.register(Sensor)
admin.site.register(Trip)