from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from DirtyDrive.models import DriveNowCarType, DriveNowCar, DriveNowChargingStation, DriveNowPetrolStation
from django.views import generic

import sys
import datetime
import dateutil.parser

from DirtyDrive import db_saver
import db_controller



def data(request):
    c = db_controller.db_controller()

    available_days_list = c.get_available_dates()

    pyv = sys.version

    if request.method == 'POST':
        the_date = dateutil.parser.parse(request.POST['Date'])

        my_db_saver = db_saver.db_saver()
        my_db_saver.run(the_date)


        return HttpResponse('Loaded '+str(the_date))
    
    context={'available_days_list': available_days_list,
        'pyv':pyv
        }

    return render(request, 'DirtyDrive/data.html', context)

def index(request):
    c = db_controller.db_controller()
    available_days_list = c.get_available_dates()
    from_day = 1
    to_day = len(available_days_list)

    if request.method == 'POST':
        from_day = int(request.POST['from_day'])
        to_day = int(request.POST['to_day'])

    print(from_day, to_day)
    DriveNowCarTypes_list = DriveNowCarType.objects.order_by('-id')
    context = {
        'DriveNowCarTypes_list': DriveNowCarTypes_list,
        'available_days_list': available_days_list,
        'from_day': from_day,
        'to_day': to_day,
        'districts': c.get_city_districts()[:10],
    }
    return render(request, 'DirtyDrive/index.html', context)

