import yfinance as yf
from stock import Stock
import pandas as pd
class Portfolio:
    """
    A class to represent a stock portfolio.
    """
    def __init__(self, stocks: list):
        """
        Initializes a new Portfolio object with a list of Stock objects. Fetch data from Yahoo Finance.
        Args:
            stocks (list): A list of Stock objects.
        """
        self.stocks = {}
        for stock in stocks:
            self.stocks.update({stock.symbol: stock})
        self.update_data()
        
        

    def update_data(self) -> None:
        """
        Fetches data from Yahoo Finance for all stocks in the portfolio.
        """
        if(len(self.stocks) == 0):
            print("No stocks in the portfolio. Exiting.")
            exit()

        self.data5y= yf.download(list(self.stocks.keys()), period = "5y")
        self.data1d= yf.download(list(self.stocks.keys()), period = "1d", interval = "1m")

        if(len(self.stocks) == 1):
            symbol = list(self.stocks.keys())[0]
            self.data5y.columns = pd.MultiIndex.from_product([self.data5y.columns, [symbol]],names=['Price', 'Ticker'])
            self.data1d.columns = pd.MultiIndex.from_product([self.data1d.columns, [symbol]],names=['Price', 'Ticker'])

        self.checkStocks()
        self.calculate_values()

    def calculate_values(self) -> None:
        """
        Update the price for each stock in the portfolio, and calculate dependent values.
        """
        for stock in self.stocks.values():
            currentPrice = self.data1d['Adj Close'][stock.symbol][-1]
            pastPrice = self.data5y['Adj Close'][stock.symbol][-6]
            stock.calculate_stock_values(currentPrice, pastPrice)
        if len(self.stocks) == 0:
            print("No stocks in the portfolio.")
            self.market_value = 0
            self.cost_price = 0
            self.total_change = 0
            self.gain_loss = 0
            past_market_value = 0
            self.weekly_change = 0
            self.pe_ratio = 0
        else:
            self.market_value = sum([stock.market_value for stock in self.stocks.values()])
            self.cost_price = sum([stock.cost_price for stock in self.stocks.values()])
            self.total_change = sum([stock.total_change for stock in self.stocks.values()])
            self.gain_loss = self.total_change / self.cost_price * 100
            past_market_value = sum([stock.qty * stock.past_price for stock in self.stocks.values()])
            self.weekly_change = ((self.market_value - past_market_value) / past_market_value) * 100
            self.pe_ratio = sum([stock.pe_ratio for stock in self.stocks.values() if stock.pe_ratio is not None]) / len([stock.pe_ratio for stock in self.stocks.values() if stock.pe_ratio is not None])

    def checkStocks(self):
        errorMsg = yf.shared._ERRORS
        errorSymbols = list(errorMsg.keys())
        for errorSymbol in errorSymbols:
            print(errorSymbol + " does not have current price available. Removed from portfolio.")
            self.remove_stock(errorSymbol)

    def add_stock(self, stock: Stock) -> None:
        """
        Adds a new stock to the portfolio.
        Args:
            stock (Stock): A Stock object to be added to the portfolio.
        """
        self.stocks.update({stock.symbol: stock})
        self.update_data()

    def remove_stock(self, stock: Stock) -> None:
        """
        Removes a stock from the portfolio.
        Args:
            stock (Stock): A Stock object to be removed from the portfolio.
        """
        del self.stocks[stock.symbol]
        self.data1d = self.data1d.drop(stock.symbol, axis=1, level='Ticker')
        self.data5y = self.data5y.drop(stock.symbol, axis=1, level='Ticker')
        self.calculate_values()
        
    def remove_stock(self, symbol: str) -> None:
        """
        Removes a stock from the portfolio.
        Args:
            symbol (str): A Stock symbol to be removed from the portfolio.
        """
        del self.stocks[symbol]
        self.data1d = self.data1d.drop(symbol, axis=1, level='Ticker')
        self.data5y = self.data5y.drop(symbol, axis=1, level='Ticker')
        self.calculate_values()

    def print_stocks(self) -> None:
        """
        Prints a summary of all stocks in the portfolio.
        """
        for stock in self.stocks.values():
            print(stock)
            print("")
    
    def summary(self) -> str:
        """
        Returns a string representation of the Portfolio object.
        """
        print(self)

    def __str__(self) -> str:
        """
        Returns a string representation of the Portfolio object.
        """
        return "\n".join([f"Portfolio Summary:",
                f"Market Value: ${self.market_value:.2f}", 
                f"Cost Basis: ${self.cost_price:.2f}", 
                f"Total Change: ${self.total_change:.2f}", 
                f"Gain/Loss: {self.gain_loss:.2f}%", 
                f"Weekly Change: {self.weekly_change:.2f}%", 
                f"Mean PE Ratio: {self.pe_ratio:.2f}"])