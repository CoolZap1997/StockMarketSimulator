from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PortfolioStockForm
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from bsedata.bse import BSE
from nsepython import *
from django.contrib import messages
from .models import *


def add_stock_to_portfolio(request):
    if request.method == 'POST':
        print("POST request received")
        form = PortfolioStockForm(request.POST)
        stock_name = form.data.get('stock_name', '').upper()  # Convert to uppercase
        if stock_name:
            stock, created = Stock.objects.get_or_create(name=stock_name)
            current_stock_value, created = CurrentStockValue.objects.get_or_create(
                stock=stock,
                defaults={'current_price': form.data.get('buy_price', "")}
            )

            if not created:
                current_stock_value.current_price = form.data.get('buy_price', "")
                current_stock_value.save()


        if form.is_valid():
            print("Form is valid")
            quantity = form.cleaned_data['quantity']
            buy_price = form.cleaned_data['buy_price']

            total_investment = buy_price * quantity

            PortfolioStock.objects.create(
                user=request.user,
                stock=stock,
                quantity=quantity,
                buy_price=buy_price,
                total_investment=total_investment
            )
            print("Portfolio entry created")
            return redirect('portfolio')
        else:
            print("Form is invalid. Reasons:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field '{field}': {error}")
            if form.non_field_errors():
                print("Non-field errors:", form.non_field_errors())

            return render(request, 'accounts/add_stock.html', {'form': form})
    else:
        form = PortfolioStockForm()
    
    return render(request, 'accounts/add_stock.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PortfolioView(View):
    def get(self, request):
        user_portfolio = PortfolioStock.objects.filter(user=request.user)

        total_investment = sum(stock.investment_value() for stock in user_portfolio)
        current_value = sum(stock.current_value() for stock in user_portfolio)

        return render(request, 'accounts/portfolio.html', {"portfolio": user_portfolio, "total_investment": total_investment, "current_value": current_value})
    

def get_bse_stock_price(stock_name):
    """Fetch stock price from BSE for numeric stock names."""
    try:
        bse_client = BSE()
        bse_data = bse_client.getQuote(stock_name)
        current_price = bse_data.get('currentValue')
        if current_price is not None:
            return JsonResponse({'current_price': current_price})
        else:
            return JsonResponse({'error': 'Price not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_nse_stock_price(stock_name):
    """Fetch stock price from NSE for non-numeric stock names."""
    try:
        print("Going to NSE")
        
        current_price = nse_eq(stock_name)['priceInfo']['lastPrice']
        if current_price is not None:
            return JsonResponse({'current_price': current_price})
        else:
            return JsonResponse({'error': 'Price not found'}, status=404)
    except Exception as e:
        print("Error in NSE")
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def get_stock_price(request):
    stock_name = request.GET.get('name')
    if stock_name.isnumeric():
        return get_bse_stock_price(stock_name)
    else:
        return get_nse_stock_price(stock_name)
    
@login_required
def withdraw_stock(request, holding_id):
    holding = get_object_or_404(PortfolioStock, id=holding_id, user=request.user)

    holding.delete()

    messages.success(request, f"Successfully withdrew your investment in {holding.stock.name}.")
    return redirect('portfolio') 