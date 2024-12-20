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
from django.utils.safestring import mark_safe

bse_client = BSE()

def add_stock_to_portfolio(request):
    if request.method == 'POST':
        print("POST request received")
        form = PortfolioStockForm(request.POST)
        stock_code = form.data.get('stock_code', '').upper()  # Convert to uppercase
        if stock_code.isnumeric():
            current_price, stock_name =  get_bse_stock_price(stock_code)
        else:
            current_price, stock_name =  get_nse_stock_price(stock_code)
        if stock_code:
            stock, created = Stock.objects.get_or_create(name=stock_code)
            if created:
                stock.company_name = stock_name
                stock.save()
            current_stock_value, created = CurrentStockValue.objects.get_or_create(
                stock=stock,
                defaults={'current_price': form.data.get('buy_price', "")}
            )

            if not created:
                current_stock_value.current_price = form.data.get('buy_price', "")
                current_stock_value.save()


        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            buy_price = form.cleaned_data['buy_price']

            PortfolioStock.objects.create(
                user=request.user,
                stock=stock,
                quantity=quantity,
                buy_price=buy_price
            )
            print("Portfolio entry created")
            return redirect('accounts:portfolio')
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

def refresh_prices(request):
    user_portfolio = PortfolioStock.objects.filter(user=request.user)
    updated_stocks = []

    for portfolio_stock in user_portfolio:
        try:
            if portfolio_stock.stock.name in updated_stocks:
                continue

            current_price = ""
            # print("\n\n\n\n\nUpdating : {}")
            if portfolio_stock.stock.name.isnumeric():
                current_price, x = get_bse_stock_price(portfolio_stock.stock.name)
            else:
                current_price, x = get_nse_stock_price(portfolio_stock.stock.name)

            current_stock_value, created = CurrentStockValue.objects.get_or_create(stock=portfolio_stock.stock)
            current_stock_value.current_price = current_price
            current_stock_value.save()

            updated_stocks.append(portfolio_stock.stock.name)
        except Exception as e:
            messages.error(request, f"Error updating {portfolio_stock.stock.name}: {e}")

    if updated_stocks:
        messages.success(request, f"Prices updated for: {', '.join(updated_stocks)}")
    else:
        messages.info(request, "No stock prices were updated.")

    return redirect('accounts:portfolio')

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PortfolioView(View):
    def get(self, request):
        # user_portfolio = PortfolioStock.objects.filter(user=request.user)

        # total_investment = sum(stock.investment_value() for stock in user_portfolio)
        # current_value = sum(stock.current_value() for stock in user_portfolio)

        # return render(request, 'accounts/portfolio.html', {"portfolio": user_portfolio, "total_investment": total_investment, "current_value": current_value})
        user_portfolio = PortfolioStock.objects.filter(user=request.user)

        total_investment = sum(stock.investment_value() for stock in user_portfolio)
        current_value = sum(stock.current_value() for stock in user_portfolio)

        stock_names = [stock.stock.name for stock in user_portfolio]
        current_prices = [stock.current_value() for stock in user_portfolio]
        current_prices_float = [float(price) for price in current_prices]
        profit_loss = [float(stock.current_value() - stock.investment_value()) for stock in user_portfolio]
        
        context = {
            "portfolio": user_portfolio,
            "total_investment": total_investment,
            "current_value": current_value,
            "stock_names": mark_safe(json.dumps(stock_names)),
            "current_prices": mark_safe(json.dumps(current_prices_float)),
            "profit_loss": mark_safe(json.dumps(profit_loss)),
        }
        return render(request, 'accounts/portfolio.html', context)

def get_bse_stock_price(stock_name):
    """Fetch stock price from BSE for numeric stock names."""
    try:
        global bse_client
        bse_data = bse_client.getQuote(stock_name)
        current_price = bse_data.get('currentValue')
        name = bse_data.get('companyName')
        return current_price, name
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_nse_stock_price(stock_name):
    """Fetch stock price from NSE for non-numeric stock names."""
    try:
        stock_details = nse_eq(stock_name)
        current_price = stock_details['priceInfo']['lastPrice']
        name = stock_details['info']['companyName']
        return current_price, name
    except Exception as e:
        print("Error in NSE")
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def get_stock_price(request):
    stock_name = request.GET.get('name')
    current_price = ''
    if stock_name.isnumeric():
        current_price, x =  get_bse_stock_price(stock_name)
    else:
        current_price, x =  get_nse_stock_price(stock_name)

    print(current_price)
    if current_price is not None:
        return JsonResponse({'current_price': current_price})
    else:
        return JsonResponse({'error': 'Price not found'}, status=404)

@login_required
def withdraw_stock(request, holding_id):
    holding = get_object_or_404(PortfolioStock, id=holding_id, user=request.user)

    holding.delete()

    messages.success(request, f"Successfully withdrew your investment in {holding.stock.name}.")
    return redirect('accounts:portfolio')
