from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Stock(models.Model):
    """Stores basic information about each stock."""
    name = models.CharField(max_length=100, unique=True)
    company_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CurrentStockValue(models.Model):
    """Stores the current market price of each stock, updated via API."""
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock.name} - {self.current_price}"

class PortfolioStock(models.Model):
    """Represents a user's investment in a specific stock."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(default=timezone.now)

    def investment_value(self):
        return self.buy_price * self.quantity

    def current_value(self):
        current_stock = CurrentStockValue.objects.get(stock=self.stock)
        return current_stock.current_price * self.quantity


    def percentage_difference(self):
        """Calculates percentage difference between current value and total investment."""
        if self.current_value() and self.investment_value():
            return ((self.current_value() - self.investment_value()) / self.investment_value()) * 100
        return 0

    def xirr(self):
        investment_date = self.created_at
        investment_amount = self.investment_value()
        current_value = self.current_value()

        current_date = timezone.now()
        days = (current_date.date() - investment_date).days

        if days < 0:
            raise ValueError("The investment date must be in the past.")

        if days == 0:
            return 0
        days_decimal = Decimal(days)
        xirr_value = ((Decimal(current_value) / Decimal(investment_amount)) ** (Decimal(365) / days_decimal) - Decimal(1)) * Decimal(100)

        return xirr_value

    def __str__(self):
        return f"{self.user.username} - {self.stock.name}"
