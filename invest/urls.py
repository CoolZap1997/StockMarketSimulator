from django.urls import path
from . import views

urlpatterns = [
    # other URL patterns
    path('add_stock/', views.add_stock, name='add_stock'),
    path('refresh/', views.refresh, name='refresh'),
    path('add_investment/', views.invest_view, name='invest_view'),
    path('withdraw_investment/', views.withdraw_view, name='withdraw_view'),
    
]
