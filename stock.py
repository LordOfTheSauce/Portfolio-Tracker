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
        self.daily_data = self.ticker.history(period="1d")
        self.weekly_data = self.ticker.history(period="1wk")

        if self.daily_data.empty:
            print(f"Warning: No price data found for ticker: {self.symbol}, setting the price and weekly change to None.")  
            self.current_price = None
            self.weekly_change = None
        else:
            self.current_price = self.daily_data['Close'][0]
            start_price = self.weekly_data['Close'].iloc[0]
            self.weekly_change = ((self.current_price - start_price) / start_price) * 100  # Percentage change
        
        self.market_value = self.qty * self.current_price 
        self.total_change = self.market_value - self.cost_price 
        self.gain_loss = self.total_change/self.cost_price * 100 

        self.pe_ratio = self.info['trailingPE'] if 'trailingPE' in self.info else None

    # def _fetch_current_price(self) -> Optional[float]:
    #     print (self.symbol)
    #     try:
    #         todays_data = self.ticker.history(period='1d')

    #         # Check if the data is genuinely available
    #         if not todays_data.empty: 
    #             return todays_data['Close'][0]
    #         else:
    #             print(f"Warning: No data found for {self.symbol}.")
    #             return 0.0 

    #     except Exception as e:  # Be specific with exception types if possible
    #         print(f"Error fetching price for {self.symbol}: {e}")
    #         return 0.0 


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

        if self.current_price is not None:
            lines.extend([
                f"Current Price: ${self.current_price:.2f}",
                f"Market Value: ${self.market_value:.2f}",
                f"Total Change: ${self.total_change:.2f}",
                f"Gain/Loss: {self.gain_loss:.2f}%"
            ])

        return "\n".join(lines)

