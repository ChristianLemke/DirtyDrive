from __future__ import unicode_literals

#from django.contrib.gis.db import models
import datetime
from django.db import models
#from django.contrib.gis.db import models



# Lat = Y Long = X

#(lng,lat)
#pnt = Point(12.4604, 43.9420)


# psql -d DirtyDriveGis -U postgres -c "CREATE EXTENSION postgis"

#python manage.py migrate
#python manage.py sqlmigrate DirtyDrive 0001

class DriveNowCarType(models.Model):
    modelIdentifier = models.CharField(db_index=True, unique=True, max_length=255)
    make = models.CharField(max_length=255)
    series = models.CharField(max_length=255)
    routingModelName = models.CharField(max_length=255)
    variant = models.CharField(max_length=255)
    carImageUrl = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    modelName = models.CharField(max_length=255)

class DriveNowCar(models.Model):
    class Meta:
        unique_together = (('datetime', 'carId', ), )
    
    
    datetime = models.DateTimeField(db_index=True, default=datetime.datetime(1970, 1, 1, 1, 1, 1), blank=True)
    carId = models.CharField(max_length=255)
    
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    licensePlate = models.CharField(max_length=255)
    transmission = models.CharField(max_length=1)
    innerCleanliness = models.CharField(max_length=255)
    isCharging = models.BooleanField()
    isPreheatable = models.BooleanField()
    isInParkingSpace = models.BooleanField()
    #parkingSpaceId = models.CharField(max_length=255)
    fuelType = models.CharField(max_length=1)
    fuelLevel = models.FloatField()
    estimatedRange = models.IntegerField()
    drivePrice = models.FloatField()
    parkPrice = models.FloatField()
    paidReservationPrice = models.FloatField()
    isOfferDrivePriceActive = models.BooleanField()
    addressStreet = models.CharField(max_length=255)
    addressZIP = models.CharField(max_length=255)
    lng = models.FloatField()
    lat = models.FloatField()
    #point = models.PointField(null=True, blank=True)
    #mPoint = django.contrib.gis.db.models.fields.MultiPointField(srid=4326)

class DriveNowChargingStation(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=255)
    address = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    lng = models.FloatField()
    lat = models.FloatField()
    #point = models.PointField(null=True, blank=True)


class DriveNowPetrolStation(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=255)
    address = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    lng = models.FloatField()
    lat = models.FloatField()
    #point = models.PointField(null=True, blank=True)

class CityDistrict(models.Model):
    id = models.IntegerField(primary_key=True)
    #polygon = models.PolygonField()
    name = models.CharField(unique=True, null=False, max_length=255)
    
