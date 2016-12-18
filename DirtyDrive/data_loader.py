# -*- coding: utf-8 -*-
import sys
import json, requests
import datetime
import dateutil.parser
import time
import shutil
import os.path
import threading

from pykml import parser
from django.contrib.gis.geos import Point, Polygon, LinearRing

from django.contrib.gis.geos import Point, GEOSGeometry
from DirtyDrive.models import DriveNowCarType, DriveNowCar, DriveNowChargingStation, DriveNowPetrolStation
from django.db import IntegrityError
from DirtyDrive.models import CityDistrict

class data_loader(object):

    def __init__(self):
        self.mydatetime = None
        self.data = None
        self.data_path = './data/'
        self.url = 'https://data.robbi5.com/drivenow-muc/'
        
        self.cars = []
        self.car_types = []
        self.charging_stations = []
        self.petrol_stations = []

        self.city_district = []

    def parse_cars(self):
        self.cars = []
        items = self.data['cars']['items']
        
        for item in items:
            dnc = DriveNowCar(
            datetime=self.mydatetime,
            carId=item['id'],
            name=item['name'],
            color=item['color'],
            licensePlate=item['licensePlate'],
            transmission=item['transmission'],
            innerCleanliness=item['innerCleanliness'],
            isCharging=item['isCharging'],
            isPreheatable=item['isPreheatable'],
            isInParkingSpace=item['isInParkingSpace'],
            #parkingSpaceId=item['parkingSpaceId'],
            fuelType=item['fuelType'],
            fuelLevel=item['fuelLevel'],
            estimatedRange=item['estimatedRange'],

            drivePrice=item['rentalPrice']['drivePrice']['amount'],
            parkPrice=item['rentalPrice']['parkPrice']['amount'],
            paidReservationPrice=item['rentalPrice']['paidReservationPrice']['amount'],
            isOfferDrivePriceActive=item['rentalPrice']['isOfferDrivePriceActive'],

            lng=item['longitude'],
            lat=item['latitude'],
            #(lng,lat)
            #pnt = Point(12.4604, 43.9420)
            point=Point(item['longitude'],item['latitude'], srid=4604),
            )

            if len(item['address']) > 0:
                dnc.addressStreet = item['address'][0]
            if len(item['address']) > 1:
                dnc.addressZIP = item['address'][1]

            self.cars.append(dnc)

        return self.cars
        
    def parse_CarTypes(self):
        self.car_types =[]
        items = self.data['carTypes']['items']
        for item in items:
            self.car_types.append(DriveNowCarType(modelIdentifier=item['modelIdentifier'],
                                                  make=item['make'],
                                                  series=item['series'],
                                                  routingModelName=item['routingModelName'],
                                                  variant=item['variant'],
                                                  carImageUrl=item['carImageUrl'],
                                                  group=item['group'],
                                                  modelName=item['modelName']
                ))
        return self.car_types

    def parse_ChargingStation(self):
        self.charging_stations = []
        items = self.data['chargingStations']['items']
        for item in items:
            self.charging_stations.append(DriveNowChargingStation(name = item['name'],
                                                address = item['address'],
                                                organisation = item['organisation'],
                                                lng = item['longitude'],
                                                lat = item['latitude'],
                                                point=Point(item['longitude'],item['latitude'], srid=4604),))
        return self.charging_stations

    def parse_PetrolStation(self):
        self.petrol_stations =[]
        items = self.data['petrolStations']['items']
        for item in items:
            self.petrol_stations.append(DriveNowPetrolStation(name = item['name'],
                                                address = item['address'],
                                                organisation = item['organisation'],
                                                lng = item['longitude'],
                                                lat = item['latitude'],
                                                point=Point(item['longitude'],item['latitude'], srid=4604),))
        return self.petrol_stations

    def get_city_districts(self):
        root = parser.fromstring(open('admins_muenchen_epsg4326.kml').read())
        self.city_district = []
        for pm in root.Document.Folder.Placemark:
            name_1 = str(pm.name).split(' ')[2]
            nr = str(pm.name).split(' ')[1]
            ring = pm.Polygon.outerBoundaryIs.LinearRing
            coords = ring.coordinates.text
            ca = coords.split(' ')
            
            points = []
            for pos in ca:
                lng, lat = pos.split(',')
                p = Point(float(lng), float(lat), srid=4326)
                points.append(p)
            
            cd = CityDistrict(
                    id = nr, 
                    name = name_1, 
                    polygon = Polygon(LinearRing(points)),
                )
            self.city_district.append(cd)

    def get_date_from_filename(self, filename):
        dateString = filename.split('muc-')[1]
        dateString = dateString.split('.json')[0]
        return dateutil.parser.parse(dateString)

    def file_exists(self, filename):
        path = self.data_path+filename.replace(':', '_')
        return os.path.exists(path)

    def download_file(self, filename):
        path = self.data_path+filename.replace(':', '_')
        r = requests.get(url=self.url + filename, stream=True)
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    def get_data(self, filename):
        # is downloaded?
        if not self.file_exists(filename):
            # download
            self.download_file(filename)
        
        path = self.data_path+filename.replace(':', '_')
        with open(path, 'r') as f:
            text = f.read()
        f.close()
        return text


    def readData(self, filename, log=True):
        # do request
        start = time.time()
        text = self.get_data(filename)
        if log:
            print('Request in %f s' % (time.time() - start))

        # read json
        start = time.time()
        data = json.loads(text)
        
        # parse it
        #RFC 3339
        self.mydatetime = self.get_date_from_filename(filename)

        self.data = data

        self.parse_cars()
        self.parse_CarTypes()
        self.parse_ChargingStation()
        self.parse_PetrolStation()
        
        if log:
            print('parse in %f s' % (time.time() - start))

    def saveData(self):
        errors =[]
        for x in self.cars, self.car_types, self.charging_stations, self.petrol_stations:
            for xx in x:
                try:
                    xx.save()
                except IntegrityError as error:
                    errors.append(error)
                except:
                    print ("Unexpected error:", sys.exc_info())
                    return
                    
        return errors
