from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import SolarData
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import calendar
from pages.forms import DateInputForm
import os
import mimetypes
from django.conf import settings
import urllib
from django.http import HttpResponse, FileResponse, Http404
from urllib.parse import unquote


def data_view(request):
    return render(request, 'data.html')


def open_file(request, file_name):
    file_name = unquote(file_name)
    # 파일 경로 생성
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'DataFile', file_name)

    if not os.path.exists(file_path):
        raise Http404("File does not exist")

# 파일 확장자에 따라 처리
    if file_name.lower().endswith('.pdf'):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="%s"' % file_name
        return response
    elif file_name.lower().endswith('.csv'):
        response = FileResponse(open(file_path, 'rb'), content_type='text/csv')
        response['Content-Disposition'] = 'inline; filename="%s"' % file_name
        return response
    else:
        raise Http404("Unsupported file type")

def get_solar_data():
    # 태양광 발전량 예측 데이터
    solar_data = SolarData.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total_projected_power_production=Sum('projected_power_production'),
        total_select_storage_battery=Sum('select_storage_battery'),
        total_select_supply_battery=Sum('select_supply_battery'),
    ).order_by('month')

    months = [calendar.month_name[data['month'].month] for data in solar_data]
    projected_power_production = [float(data['total_projected_power_production']) for data in solar_data]
    select_storage_battery = [float(data['total_select_storage_battery']) for data in solar_data]
    select_supply_battery = [float(data['total_select_supply_battery']) for data in solar_data]

    return months, projected_power_production, select_storage_battery, select_supply_battery


def get_battery_data(month, day):
    if not month or not day:
        return [], [], []

    # 연도 2022로 설정
    year = 2022
    start_datetime = datetime(year, int(month), int(day), 0, 0)
    end_datetime = start_datetime + timedelta(days=1)

    # 데이터 필터링
    data = SolarData.objects.filter(date__range=[start_datetime, end_datetime])

    # 데이터 처리
    time_labels = []
    short_battery = []
    long_battery = []

    for entry in data:
        time_labels.append(entry.date.strftime("%H:%M"))
        short_battery.append(entry.curr_short_battery)
        long_battery.append(entry.curr_long_battery)

    return time_labels, short_battery, long_battery


def mainpage(request):
    selected_month = None
    selected_day = None

    # 배터리 데이터 가져오기 - `mainpage.html`에도 필요하므로 그대로 유지합니다.
    current_time = now()
    battery_data = SolarData.objects.filter(date__month=current_time.month,
                                            date__day=current_time.day,
                                            date__hour=current_time.hour).first()

    # 전체 배터리 용량
    total_short_battery_capacity = 9916.665
    total_long_battery_capacity = 1000000

    # 백분율 계산
    if battery_data:
        short_battery_percentage = (battery_data.curr_short_battery / total_short_battery_capacity) * 100
        long_battery_percentage = (battery_data.curr_long_battery / total_long_battery_capacity) * 100
    else:
        short_battery_percentage = long_battery_percentage = 0  # 데이터가 없을 경우 0으로 설정

    # 태양광 발전량 예측 데이터 가져오기
    months, projected_power_production, select_storage_battery, select_supply_battery = get_solar_data()

    # Context 데이터 준비
    context = {
        'months': months,
        'projected_power_production': projected_power_production,
        'select_storage_battery': select_storage_battery,
        'select_supply_battery': select_supply_battery,
        'short_battery_percentage': short_battery_percentage,
        'long_battery_percentage': long_battery_percentage,
    }

    return render(request, 'pages/mainpage.html', context)


def battery_data_json(request):
    month = request.GET.get('month')
    day = request.GET.get('day')

    # 배터리 데이터 가져오기
    time_labels, short_battery, long_battery = get_battery_data(month, day)

    # JSON 응답
    response_data = {
        'time_labels': time_labels,
        'short_battery': short_battery,
        'long_battery': long_battery,
    }
    return JsonResponse(response_data)


def battery(request):
    selected_month = request.GET.get('month')
    selected_day = request.GET.get('day')

    # 배터리 데이터 가져오기
    time_labels, short_battery, long_battery = get_battery_data(selected_month, selected_day)

    # 현재 시간에 따른 배터리 데이터 가져오기
    current_time = now()
    battery_data = SolarData.objects.filter(date__month=current_time.month,
                                            date__day=current_time.day,
                                            date__hour=current_time.hour).first()

    # 전체 배터리 용량
    total_short_battery_capacity = 9916.665
    total_long_battery_capacity = 1000000

    # 백분율 계산
    if battery_data:
        short_battery_percentage = (battery_data.curr_short_battery / total_short_battery_capacity) * 100
        long_battery_percentage = (battery_data.curr_long_battery / total_long_battery_capacity) * 100
    else:
        short_battery_percentage = long_battery_percentage = 0  # 데이터가 없을 경우 0으로 설정

    context = {
        'time_labels': time_labels,
        'short_battery': short_battery,
        'long_battery': long_battery,
        'short_battery_percentage': short_battery_percentage,
        'long_battery_percentage': long_battery_percentage,
    }
    return render(request, 'pages/battery.html', context)


def lamp(request):
    return render(request, 'pages/lamp.html')

def data(request):
    return render(request, 'pages/data.html')
