from typing import Optional
import yfinance as yf

class Stock:
    """
    A class to represent a stock holding (with type hints).
    """

    def __init__(self, symbol: str, qty: float, cost_per_share: float):
        """
        Initializes a new Stock object with user-provided input.

        Args:
            symbol (str): The stock symbol.
            qty (float): The number of shares held.
            cost_per_share (float): The cost per share of the stock.
        """
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.info = self.ticker.info
        if 'symbol' not in self.info:
            raise ValueError(f"No data found for ticker: {self.symbol}")
        self.qty = qty
        self.cost_per_share = cost_per_share
        self.company_name = self.info['longName']
        self.__calclate_values__()  # Calculate dependent values

    def __calclate_values__(self) -> None:
        """
        Calculates dependent values based on the provided input.
        """
        self.cost_price: float = self.qty * self.cost_per_share
        self.weekly_data = self.ticker.history(period="1wk")
        self.daily_data = self.ticker.history(period="1d")

        try:
            self.current_price = self.daily_data['Close'].iloc[0]
            self.past_price = self.weekly_data['Close'].iloc[0]
            self.weekly_change = ((self.current_price - self.past_price) / self.past_price) * 100  # Percentage change
            self.market_value = self.qty * self.current_price 
            self.total_change = self.market_value - self.cost_price 
            self.gain_loss = self.total_change/self.cost_price * 100 
            self.pe_ratio = self.info['trailingPE'] if 'trailingPE' in self.info else 0

        except IndexError:
            self.current_price = 0
            self.past_price = 0
            self.weekly_change = 0
            self.market_value = 0
            self.total_change = 0
            self.gain_loss = 0
            self.pe_ratio = None
            print(f"Warning: No current price found for {self.symbol}, setting all values to 0.")

    def __str__(self) -> str:
        """
        Returns a string representation of the Stock object.
        """
        lines = [
            f"Company: {self.company_name} ({self.symbol})",
            f"Shares: {self.qty}",
            f"Cost per Share: ${self.cost_per_share:.2f}",
            f"Cost Basis: ${self.cost_price:.2f}",
        ]

        if self.current_price != 0:
            lines.extend([
                f"Current Price: ${self.current_price:.2f}",
                f"Market Value: ${self.market_value:.2f}",
                f"Total Change: ${self.total_change:.2f}",
                f"Gain/Loss: {self.gain_loss:.2f}%",
                f"Weekly Change: {self.weekly_change:.2f}%",
                f"PE Ratio: {self.pe_ratio}"
            ])
        else:
            lines.append("Warning: No current price found for this stock.")

        return "\n".join(lines)

