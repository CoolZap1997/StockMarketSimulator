from django import forms
from .models import PortfolioStock, Stock

class PortfolioStockForm(forms.ModelForm):
    stock_code = forms.CharField(label='Stock Code', max_length=100, required=True)
    quantity = forms.DecimalField(decimal_places=2)
    buy_price = forms.DecimalField(label='Buy Price', max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = PortfolioStock
        fields = ['quantity', 'buy_price']  # Exclude stock_code from the model fields

    def clean_stock_code(self):
        """Clean and validate the stock name input."""
        stock_code = self.cleaned_data['stock_code']
        try:
            # Check if the stock exists
            Stock.objects.get(name=stock_code)
        except Stock.DoesNotExist:
            raise forms.ValidationError("Stock does not exist. Please enter a valid stock name.")
        return stock_code
