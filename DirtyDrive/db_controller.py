# -*- coding: utf-8 -*-
import sys
import datetime
import time
from django.db import IntegrityError
import shutil

from DirtyDrive.models import CityDistrict, DriveNowCarType, DriveNowCar, DriveNowChargingStation, DriveNowPetrolStation
from django.db.models import Count, Avg
from django.db.models.functions import TruncDay

class db_controller(object):

    def __init__(self):
        self.cars = []
        self.car_types = []
        self.charging_stations = []
        self.petrol_stations = []

    def get_available_dates(self):
        days = DriveNowCar.objects.annotate(day=TruncDay('datetime'))\
            .values('day').annotate(available=Count('datetime'))
        days = days.order_by('day')

        return [x for x in days]

    def get_city_districts(self):
        districts = CityDistrict.objects.all().order_by('id')
        return [x for x in districts]