import yfinance as yf
import numpy as np

class Stock:
    """
    A class to represent a stock holding.
    """

    def __init__(self, symbol: str, qty, cost_per_share):
        """
        Initializes a new Stock object with a quantity (list) and a price (list).

        Args:
            symbol (str): The stock symbol.
            qty (float or list): The number of shares held, or a list of quantities.
            cost_per_share (float or list): The cost per share of the stock, or a list of costs.
        """
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol,)
        self.info = self.ticker.info
        if 'symbol' not in self.info:
            raise ValueError(f"No data found for ticker: {self.symbol}")
        self.company_name = self.info['longName']
        self.pe_ratio = self.info['trailingPE'] if 'trailingPE' in self.info else 0
        if isinstance(qty,(int,float)) and isinstance(cost_per_share,(int,float)):
            self.qtys = []
            self.costs_per_share = []
            self.qtys.append(qty)
            self.costs_per_share.append(cost_per_share)
        elif type(qty) == list and type(cost_per_share) == list:
            if len(qty) != len(cost_per_share):
                raise ValueError("Length of qtys and costs_per_share must be the same")
            self.qtys = qty
            self.costs_per_share = cost_per_share
        else:
            raise TypeError()

    def add_to_stock(self,qty, cost_per_share) -> None:
        """
        Adds more shares to the stock, with a single quantity and a single price, or a list of quantities and a list of prices.
        """
        if isinstance(qty,(int,float)) and isinstance(cost_per_share,(int,float)):
            self.qtys.append(qty)
            self.costs_per_share.append(cost_per_share)
        elif type(qty) == list and type(cost_per_share) == list:
            if len(qty) != len(cost_per_share):
                raise ValueError("Length of qtys and costs_per_share must be the same")
            self.qtys.extend(qty)
            self.costs_per_share.extend(cost_per_share)
        else:
            raise TypeError()
        
    def calculate_stock_values(self,currentPrice,pastPrice) -> None:
        """
        Calculates dependent values based on the provided input.
        """
        self.qty = sum(self.qtys)
        self.base_cost = np.dot(self.qtys,self.costs_per_share)
        self.cost_per_share = self.base_cost / self.qty
        self.current_price = currentPrice
        self.past_price = pastPrice
        self.weekly_change = ((self.current_price - self.past_price) / self.past_price) * 100  # Percentage change
        self.market_value = self.qty * self.current_price 
        self.total_change = self.market_value - self.base_cost 
        self.gain_loss = self.total_change/self.base_cost * 100 
        
    def __str__(self) -> str:
        """
        Returns a string representation of the Stock object.
        """
        lines = [
            f"Company: {self.company_name} ({self.symbol})",
            f"Shares: {self.qty}",
            f"Average Cost per Share: ${self.cost_per_share:.2f}",
            f"Cost Basis: ${self.base_cost:.2f}",
            f"Current Price: ${self.current_price:.2f}",
            f"Market Value: ${self.market_value:.2f}",
            f"Total Change: ${self.total_change:.2f}",
            f"Gain/Loss: {self.gain_loss:.2f}%",
            f"Weekly Change: {self.weekly_change:.2f}%",
            f"PE Ratio: {self.pe_ratio}"
            ]
        return "\n".join(lines)

