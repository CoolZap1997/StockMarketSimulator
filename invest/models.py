from django.db import models
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint
from datetime import date

class Stocks(models.Model):
    stock_name = models.CharField(max_length=255, unique=True)
    stock_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.stock_name

class Transaction(models.Model):
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    date = models.DateField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    number_of_stocks = models.PositiveIntegerField()

    def current_value(self):
        return int(self.number_of_stocks) * float(self.stock.stock_price)
    
    def investment_value(self):
        return int(self.number_of_stocks) * float(self.cost_price)
    
    def percentage_difference(self):
        total_investment = self.investment_value()
        current_value = self.current_value()
        if total_investment == 0:
            return 0
        return ((current_value - total_investment) / total_investment) * 100
    
    def xirr(self):
        duration = (date.today() - self.date).days
        total_investment = self.investment_value()
        total_value = self.current_value()
        profit_or_loss = total_value - total_investment
        # print(profit_or_loss)
        # print(type(profit_or_loss))
        print("Duration: " + str(duration))
        print(type(duration))
        if duration == 0:
            duration = 1
        time_factor = 365 / duration
        return float(profit_or_loss * time_factor * 100) / total_investment

    def __str__(self):
        return f"Transaction for {self.stock.stock_name} on {self.date}"
