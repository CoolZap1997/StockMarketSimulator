# Stock Market Simulation App

## Overview

The Stock Market Simulation App is a Django-based web application that allows users to simulate stock trading by managing a portfolio of stocks. Users can add stocks to their portfolio, check current stock prices, calculate investment metrics such as percentage difference and XIRR, and visualize their investment performance.

## Features

- **User Authentication**: Secure login and registration for users.
- **Portfolio Management**: Users can add stocks to their portfolio with the option to input the stock name, quantity, and buy price.
- **Current Stock Price Retrieval**: Stock prices are fetched from an external API, allowing users to see the current value of their investments.
- **Investment Metrics**: Calculate and display:
  - **Percentage Difference**: Shows how much the current value of the investment has changed from the buy price.
  - **XIRR**: Calculates the extended internal rate of return for the investment over time.
- **Withdrawal Functionality**: Users can withdraw their investments with a confirmation prompt.

Installation

mkdir stock_simulator
git clone https://github.com/CoolZap1997/StockMarketSimulator.git
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Enjoy investing in the virtual risk free stock market

