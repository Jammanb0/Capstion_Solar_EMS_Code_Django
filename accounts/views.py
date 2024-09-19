from django.views.generic import ListView
from .models import SolarData


class SolarDataListView(ListView):
    model = SolarData
    template_name = 'accounts/solar_data_list.html'
    context_object_name = 'solar_data_list'
