from django.db import models

class SolarData(models.Model):
    date = models.DateTimeField()
    ac_w = models.FloatField()
    curr_short_battery = models.FloatField()
    curr_long_battery = models.FloatField()
    projected_power_production = models.FloatField()
    season = models.IntegerField()
    predicted_power_consumption = models.FloatField()
    select_storage_battery = models.CharField(max_length=50)
    select_supply_battery = models.CharField(max_length=50)
    light_control = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.ac_w}W"