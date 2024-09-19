from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mainpage, name='mainpage'),
    path('battery/', views.battery),
    path('lamp/', views.lamp),
    path('data/', views.data),
    path('battery-data-json/', views.battery_data_json, name='battery_data_json'),
    path('open_file/<str:file_name>', views.open_file, name='open_file'),
    path('data/', views.data_view, name='data_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)