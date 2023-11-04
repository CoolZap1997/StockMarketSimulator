from django.shortcuts import render
from .models import Stocks, Transaction
from .one_stock import find_stock_price
from django.http import JsonResponse
from decimal import Decimal
from django.utils import timezone


def add_stock(request):
    error_message = ''
    success_message = ''
    if request.method == 'POST':
        stock_name = request.POST['stock_name']

        # Convert the stock name to lowercase for case-insensitive comparison
        existing_stock = Stocks.objects.filter(stock_name__iexact=stock_name).first()

        if existing_stock:
            error_message = f'Stock with the name {stock_name} already exists.'
        else:
            stock_price = find_stock_price(stock_name)
            stock = Stocks(stock_name=stock_name, stock_price=stock_price)
            stock.save()

    # Fetch all stocks from the database
    stocks = Stocks.objects.all()
    investments = Transaction.objects.all()

    return render(request, 'invest/add_stock.html', {'stocks': stocks, 'investments': investments, "errorMsg":error_message, "successMsg":success_message})

def invest_view(request):
    if request.method == 'POST':
        stock_id = int(request.POST.get('stock_id').replace("stock-", ""))
        number_of_stocks = int(request.POST.get('number_of_stocks'))
        print(stock_id)
        print(type(stock_id))
        print(number_of_stocks)
        print(type(number_of_stocks))

        stock = Stocks.objects.get(id=stock_id)

        current_date = timezone.now()
        stock_price = find_stock_price(stock.stock_name)
        stock.stock_price = stock_price
        total_cost_price = float(stock_price) * number_of_stocks
        transaction = Transaction(
            stock=stock,
            date=current_date,
            cost_price=stock_price,
            number_of_stocks=number_of_stocks
        )
        transaction.save()

        return JsonResponse({'message': 'Investment successful!'}, status=201)

    # Handle other HTTP methods or invalid requests
    return JsonResponse({'message': 'Invalid request.'}, status=400)


def withdraw_view(request):
    if request.method == 'POST':
        investment_id = int(request.POST.get('investmentId').replace("investment-", ""))
        number_of_stocks = int(request.POST.get('number_of_stocks'))
        # print(investment_id)
        # print(type(investment_id))
        # print(number_of_stocks)
        # print(type(number_of_stocks))

        investment = Transaction.objects.get(id=investment_id)
        investment_number_of_stocks = investment.number_of_stocks
        # print(investment_number_of_stocks)
        # print(type(investment_number_of_stocks))

        if number_of_stocks == investment_number_of_stocks:
            investment.delete()
        else:
            investment.number_of_stocks -= number_of_stocks
            print(investment.number_of_stocks)
            print(type(investment.number_of_stocks))
            investment.save()

        return JsonResponse({'message': 'Investment successful!'}, status=201)

    # Handle other HTTP methods or invalid requests
    return JsonResponse({'message': 'Invalid request.'}, status=400)


def refresh(request):
    error_message = ''
    success_message = ''

    # Convert the stock name to lowercase for case-insensitive comparison
    all_stocks = Stocks.objects.all()
    
    for stock in all_stocks:
        stock_price = find_stock_price(stock.stock_name)
        stock.stock_price=stock_price
        stock.save()

    # Fetch all stocks from the database
    stocks = Stocks.objects.all()
    investments = Transaction.objects.all()

    return render(request, 'invest/add_stock.html', {'stocks': stocks, 'investments': investments, "errorMsg":error_message, "successMsg":success_message})

