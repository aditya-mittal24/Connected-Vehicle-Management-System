# Generated by Django 5.1.1 on 2024-09-21 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('owner_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('contact_info', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('vehicle_id', models.AutoField(primary_key=True, serialize=False)),
                ('make', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('fuel_type', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CVMS.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('trip_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('start_location', models.CharField(max_length=255)),
                ('end_location', models.CharField(max_length=255)),
                ('distance_traveled', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CVMS.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.AutoField(primary_key=True, serialize=False)),
                ('sensor_type', models.CharField(max_length=100)),
                ('sensor_reading', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField()),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CVMS.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('maintenance_id', models.AutoField(primary_key=True, serialize=False)),
                ('maintenance_type', models.CharField(max_length=255)),
                ('maintenance_date', models.DateField()),
                ('maintenance_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CVMS.vehicle')),
            ],
        ),
    ]
