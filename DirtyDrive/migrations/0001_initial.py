# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-09 17:00
from __future__ import unicode_literals

import datetime
import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DriveNowCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, db_index=True, default=datetime.datetime(1970, 1, 1, 1, 1, 1))),
                ('carId', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('licensePlate', models.CharField(max_length=255)),
                ('transmission', models.CharField(max_length=1)),
                ('innerCleanliness', models.CharField(max_length=255)),
                ('isCharging', models.BooleanField()),
                ('isPreheatable', models.BooleanField()),
                ('isInParkingSpace', models.BooleanField()),
                ('fuelType', models.CharField(max_length=1)),
                ('fuelLevel', models.FloatField()),
                ('estimatedRange', models.IntegerField()),
                ('drivePrice', models.FloatField()),
                ('parkPrice', models.FloatField()),
                ('paidReservationPrice', models.FloatField()),
                ('isOfferDrivePriceActive', models.BooleanField()),
                ('addressStreet', models.CharField(max_length=255)),
                ('addressZIP', models.CharField(max_length=255)),
                ('lng', models.FloatField()),
                ('lat', models.FloatField()),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='DriveNowCarType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelIdentifier', models.CharField(db_index=True, max_length=255, unique=True)),
                ('make', models.CharField(max_length=255)),
                ('series', models.CharField(max_length=255)),
                ('routingModelName', models.CharField(max_length=255)),
                ('variant', models.CharField(max_length=255)),
                ('carImageUrl', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=255)),
                ('modelName', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DriveNowChargingStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('organisation', models.CharField(max_length=255)),
                ('lng', models.FloatField()),
                ('lat', models.FloatField()),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='DriveNowPetrolStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('organisation', models.CharField(max_length=255)),
                ('lng', models.FloatField()),
                ('lat', models.FloatField()),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='drivenowcar',
            unique_together=set([('datetime', 'carId')]),
        ),
    ]