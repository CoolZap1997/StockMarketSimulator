from django.contrib import admin
from .models import Stocks, Transaction

admin.site.register(Stocks)
admin.site.register(Transaction)