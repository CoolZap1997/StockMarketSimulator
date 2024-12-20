# accounts/urls.py
from django.urls import path
from .views import RegisterView, PortfolioView, get_stock_price, add_stock_to_portfolio, withdraw_stock, refresh_prices
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('add-stock/', add_stock_to_portfolio, name='add_stock'),
    path('get_stock_price', get_stock_price, name='get_stock_price'),
    path('withdraw/<int:holding_id>/', withdraw_stock, name='withdraw_stock'),
    path('refresh_prices/', refresh_prices, name='refresh_prices'),
]
