import yfinance as yf
from stock import Stock
class Portfolio:
    """
    A class to represent a stock portfolio.
    """
    def __init__(self, stocks: list):
        """
        Initializes a new Portfolio object with user-provided input.
        Args:
            stocks (list): A list of Stock objects.
        """
        self.stocks = stocks
        self.tickers = [stock.ticker for stock in stocks]
        self.__calculate_values__()

    def __calculate_values__(self) -> None:
        """
        Calculates dependent values based on the provided input.
        """
        self.market_value = sum([stock.market_value for stock in self.stocks])
        self.cost_price = sum([stock.cost_price for stock in self.stocks])
        self.total_change = sum([stock.total_change for stock in self.stocks])
        self.gain_loss = self.total_change / self.cost_price * 100
        past_market_value = sum([stock.qty * stock.past_price for stock in self.stocks])
        self.weekly_change = ((self.market_value - past_market_value) / past_market_value) * 100
        self.pe_ratio = sum([stock.pe_ratio for stock in self.stocks if stock.pe_ratio is not None]) / len([stock.pe_ratio for stock in self.stocks if stock.pe_ratio is not None])

    def add_stock(self, stock: Stock) -> None:
        """
        Adds a new stock to the portfolio.
        Args:
            stock (Stock): A Stock object to be added to the portfolio.
        """
        self.stocks.append(stock)
        self.tickers.append(stock.ticker)
        self.__calculate_values__()

    def remove_stock(self, stock: Stock) -> None:
        """
        Removes a stock from the portfolio.
        Args:
            stock (Stock): A Stock object to be removed from the portfolio.
        """
        self.stocks.remove(stock)
        self.tickers.remove(stock.ticker)
        self.__calculate_values__()

    def print_stocks(self) -> None:
        """
        Prints a summary of all stocks in the portfolio.
        """
        for stock in self.stocks:
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
                f"PE Ratio: {self.pe_ratio:.2f}"])