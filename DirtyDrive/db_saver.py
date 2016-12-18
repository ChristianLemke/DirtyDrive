# -*- coding: utf-8 -*-
import django, os

from DirtyDrive import data_loader as loader
import json, requests
from lxml import html
import datetime
import time
import pytz
import threading

class db_saver(object):

    def __init__(self):
        self.url = 'https://data.robbi5.com/drivenow-muc/'
        self.page_dates = []
        self.filtered_page_dates = []
        self.dl = loader.data_loader()

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DirtyDrive.settings')
        #settings.configure()
        django.setup()
    
    def save_city_districts(self):
        self.dl.get_city_districts()
        for x in self.dl.city_district:
            x.save()

    def load_filenames(self):
        page = requests.get(url=self.url)
        self.page_dates = []

        if page.status_code == 200:
            tree = html.fromstring(page.content)
            page_json_files = tree.xpath('/html/body/pre/a/text()')

        for t in page_json_files[1:]:
            self.page_dates.append([self.dl.get_date_from_filename(t),t])
    
    def filter_dates(self, day, minutes):
        self.filtered_page_dates = []
        
        for d, file_name in self.page_dates:
            if d.year==day.year and d.month==day.month and d.day==day.day:
                if(d.minute in minutes):
                    self.filtered_page_dates.append(file_name)

    def save_filter_dates(self, log=True):
        for file_name in self.filtered_page_dates:
            print(file_name)
            
            self.dl.readData(file_name, log)
            
            start = time.time()
            self.dl.saveData()
            if log:
                print('db save in %f s' % (time.time() - start))

    def download_by_threads(self, filenames):
        # subparts
        n= 8
        l = filenames
        for sublist in [l[i:i + n] for i in xrange(0, len(l), n)]:
            print('Downloading: '+str(sublist))
            # thread download 
            threads = [threading.Thread(target=self.dl.download_file, args=(filename,)) 
                    for filename in sublist]

            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

    def run(self, day):
        self.load_filenames()

        #minutes = [0,15,30,45]
        minutes = [0,10,20,30,40,50]
        #minutes = [0,5,10,15,20,25,30,35,40,45,50,55]
        self.filter_dates(day, minutes)

        files = [x for x in self.filtered_page_dates if not self.dl.file_exists(x)]
        
        self.download_by_threads(files)
        self.save_filter_dates(log=True)

    
        
