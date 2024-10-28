from django.contrib import admin
from .models import Stock, CurrentStockValue, PortfolioStock


# Register your models here
admin.site.register(Stock)
admin.site.register(CurrentStockValue)
admin.site.register(PortfolioStock)