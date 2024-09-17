import yfinance as yf
import pandas as pd
from datetime import datetime

# Input
ticker_symbol = input("Enter Ticker Symbol:").strip()
stock = yf.Ticker(ticker_symbol)


# General Values
company_name = stock.info.get('longName', 'Not Available')
industry = stock.info.get('industry', 'Not Available')
market_cap = stock.info.get('marketCap', 'Not Available')
formatted_market_cap = "{:,}".format(market_cap) if isinstance(market_cap, (int, float)) else "Not Available"


# Historical Data
balance_sheet = stock.balance_sheet


# Get available dates
available_dates = balance_sheet.columns


# Map dates to specific years
cash_data = {}
debt_data = {}

for date in available_dates:
    year = pd.to_datetime(date).year
    cash_amount = balance_sheet.loc['Cash And Cash Equivalents', date]
    debt_amount = balance_sheet.loc['Total Debt', date]

# Format with commas and convert to string
    cash_data[str(year)] = "{:,}".format(int(cash_amount)) if not pd.isna(cash_amount) else 'N/A'
    debt_data[str(year)] = "{:,}".format(int(debt_amount)) if not pd.isna(debt_amount) else 'N/A'


# Retrieve Present Data (2024)
present_cash_data = stock.info.get('totalCash', 'N/A')
present_debt_data = stock.info.get('totalDebt', 'N/A')


# Format with commas and convert to string
cash_data['2024'] = "{:,}".format(int(present_cash_data)) if isinstance(present_cash_data, (int, float)) else 'N/A'
debt_data['2024'] = "{:,}".format(int(present_debt_data)) if isinstance(present_debt_data, (int, float)) else 'N/A'


# Single-Year Data
trailing_pe_data = stock.info.get('trailingPE', 'N/A')
formatted_trailing_pe = "{:,.2f}".format(trailing_pe_data) if isinstance(trailing_pe_data, (int, float)) else "N/A"

forward_pe_data = stock.info.get('forwardPE', 'N/A')
formatted_forward_pe = "{:,.2f}".format(forward_pe_data) if isinstance(forward_pe_data, (int, float)) else "N/A"

price_to_book_data = stock.info.get('priceToBook', 'N/A')
formatted_price_to_book = "{:,.2f}".format(price_to_book_data) if isinstance(price_to_book_data, (int, float)) else "N/A"

free_cashflow_data = stock.info.get('freeCashflow', 'N/A')
formatted_price_to_free_cashflow = "{:,.2f}".format(market_cap / free_cashflow_data) if isinstance(free_cashflow_data, (int, float)) and free_cashflow_data > 0 else "Not Available"


# Today's Date
today_date = datetime.today()
formatted_date = today_date.strftime("%Y-%m-%d |")


# Unavailable Data (Non-Present Day Trailing P/E, Forward P/E, P/B Ratio, and P/FC Ratio)
na_data = "N/A"

# DataFrame
financial_data = pd.DataFrame({
    formatted_date: [
        cash_data.get('2024', 'N/A'),
        debt_data.get('2024', 'N/A'),
        formatted_trailing_pe,
        formatted_forward_pe,
        formatted_price_to_book,
        formatted_price_to_free_cashflow
    ],
    '2023-09-30 |': [
        cash_data.get('2023', 'N/A'),
        debt_data.get('2023', 'N/A'),
        na_data,
        na_data,
        na_data,
        na_data
    ],
    '2022-09-30 |': [
        cash_data.get('2022', 'N/A'),
        debt_data.get('2022', 'N/A'),
        na_data,
        na_data,
        na_data,
        na_data
    ],
    '2021-09-30 |': [
        cash_data.get('2021', 'N/A'),
        debt_data.get('2021', 'N/A'),
        na_data,
        na_data,
        na_data,
        na_data
    ],
}, index=['Cash on Hand', 'Total Debt', 'Trailing P/E', 'Forward P/E', 'P/B Ratio', 'P/FC Ratio'])

# Transpose DataFrame
financial_data = financial_data.T

# Output
print(f"Ticker Symbol: {ticker_symbol}")
print(f"Company Name: {company_name}")
print(f"Industry: {industry}")
print(f"Market Cap: {formatted_market_cap}")
print("")

print(financial_data.to_string())
