from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
    path('solar-data/', views.SolarDataListView.as_view(), name='solar_data_list'),
    # '/solar-data/' URL로 요청이 들어오면 SolarDataListView를 사용
    ]