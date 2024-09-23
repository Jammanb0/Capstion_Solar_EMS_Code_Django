import csv
from django.core.management.base import BaseCommand
from accounts.models import SolarData
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = 'Load data from CSV file into the database'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\LG\Desktop\2024\Capstone\데이터\실제 사용 데이터\최종\한계를 최소로\pv4_2022_final_최종_태양광 예측 반영본_한계돌파 최소 추가.csv'
        timezone = pytz.timezone('Asia/Seoul')

        error_count = 0  # 오류 카운트 변수
        all_successful = True  # 모든 행이 성공적으로 처리되었는지 추적

        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            headers = reader.fieldnames
            print("CSV 파일의 열 이름:", headers)

            for row in reader:
                print("Processing row:", row)  # 현재 처리 중인 행을 출력
                date_str = row['date']

                try:
                    # 시간 부분이 한 자리일 경우 앞에 0을 추가하는 로직
                    if len(date_str.split(' ')[1]) == 4:  # 'H:MM' 형식
                        date_str = date_str.replace(' ', ' 0', 1)

                    # 초가 포함되지 않은 날짜 형식 처리 추가
                    if len(date_str) == 16:  # 'YYYY-MM-DD HH:MM' 형식
                        naive_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                    else:  # 'YYYY-MM-DD HH:MM:SS' 형식
                        naive_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

                    aware_datetime = timezone.localize(naive_datetime)
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f'Invalid date format for row: {row}, error: {e}'))
                    error_count += 1
                    all_successful = False
                    continue

                try:
                    # CSV 파일의 데이터를 데이터베이스에 저장
                    SolarData.objects.create(
                        date=aware_datetime,
                        ac_w=float(row['AC_W']),
                        curr_short_battery=float(row['Curr_Short_Battery']),
                        curr_long_battery=float(row['Curr_Long_Battery']),
                        projected_power_production=float(row['Projected_Power_Production']),
                        season=int(row['Season']),
                        predicted_power_consumption=float(row['Predicted_Power_Consumption']),
                        select_storage_battery=row['Select_Storage_Battery'],
                        select_supply_battery=row['Select_Supply_Battery'],
                        light_control=int(row['Light_Control'])
                    )
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f'Value error for row: {row}, error: {e}'))
                    error_count += 1
                    all_successful = False
                    continue

        if all_successful:
            self.stdout.write(self.style.SUCCESS('Successfully loaded data into the database'))
        else:
            self.stdout.write(self.style.ERROR(f'Data loading completed with {error_count} errors.'))
