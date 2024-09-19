from django.contrib import admin
from .models import SolarData

@admin.register(SolarData)
class SolarDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'ac_w', 'curr_short_battery', 'curr_long_battery', 'projected_power_production', 'season', 'predicted_power_consumption', 'select_storage_battery', 'select_supply_battery', 'light_control')

    list_filter = ('date', 'season')
    search_fields = ('date',)