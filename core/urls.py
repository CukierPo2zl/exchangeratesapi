from django.urls import path
from core.views import get_supported_currencies, get_plot_data, get_latest, get_symbols_with_countries

urlpatterns = [
    path('currencies/', get_supported_currencies),
    path('rates/', get_plot_data),
    path('latest/', get_latest),
    path('symbols/', get_symbols_with_countries),

]
