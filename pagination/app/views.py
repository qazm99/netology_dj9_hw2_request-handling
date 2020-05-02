from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
import csv


def index(request):
    return redirect(reverse(bus_stations))

def get_bus_station_from_csv(filename):
    with open(filename, newline='', encoding='cp1251') as file:
        data_bus_station = csv.DictReader(file, delimiter=';')
        list_bus_station = list(data_bus_station)
        # for bus_stat in list_bus_station:
        #     print(bus_stat)
    return list_bus_station


def bus_stations(request):
    data_bus_stations = get_bus_station_from_csv(settings.BUS_STATION_CSV)
    pagunator_bus_station = Paginator(data_bus_stations, 10)

    current_page = int(request.GET.get('page', 1))
    if current_page > pagunator_bus_station.num_pages:
        current_page = pagunator_bus_station.num_pages
    current_bus_stations = pagunator_bus_station.get_page(current_page)
    #print(current_bus_station.object_list)

    if current_bus_stations.has_next():
        next_page_url = f'?page={current_bus_stations.next_page_number()}'
    else:
        next_page_url = ''
    if current_bus_stations.has_previous():
        prev_page_url = f'?page={current_bus_stations.previous_page_number()}'
    else:
        prev_page_url = ''
    range_many_page = 100
    if current_page - range_many_page < 1:
        prev10_page_url = ''
    else:
        prev10_page_url = f'?page={current_page - range_many_page}'
    if current_page + range_many_page > pagunator_bus_station.num_pages:
        next10_page_url = ''
    else:
        next10_page_url = f'?page={current_page + range_many_page}'
    bus_stations_list = list(map(lambda cur_bus_stat: {'Name': cur_bus_stat.get('Name'),
                                                       'Street': cur_bus_stat.get('Street'),
                                                       'District': cur_bus_stat.get('District')},
                                 current_bus_stations))

    return render_to_response('index.html', context={
        'bus_stations': bus_stations_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
        'prev10_page_url': prev10_page_url,
        'next10_page_url': next10_page_url,
        'first_page_url': '?page=1',
        'end_page_url': f'?page={pagunator_bus_station.num_pages}',
        'end_page': pagunator_bus_station.num_pages,
    })

