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
        self.ticker = yf.Ticker(symbol,)
        self.info = self.ticker.info
        if 'symbol' not in self.info:
            raise ValueError(f"No data found for ticker: {self.symbol}")
        self.qty = qty
        self.cost_per_share = cost_per_share
        self.company_name = self.info['longName']
        self.cost_price = self.qty * self.cost_per_share
        self.pe_ratio = self.info['trailingPE'] if 'trailingPE' in self.info else 0

    def calculate_stock_values(self,currentPrice,pastPrice) -> None:
        """
        Calculates dependent values based on the provided input.
        """
        self.current_price = currentPrice
        self.past_price = pastPrice
        self.weekly_change = ((self.current_price - self.past_price) / self.past_price) * 100  # Percentage change
        self.market_value = self.qty * self.current_price 
        self.total_change = self.market_value - self.cost_price 
        self.gain_loss = self.total_change/self.cost_price * 100 
        
    def __str__(self) -> str:
        """
        Returns a string representation of the Stock object.
        """
        lines = [
            f"Company: {self.company_name} ({self.symbol})",
            f"Shares: {self.qty}",
            f"Cost per Share: ${self.cost_per_share:.2f}",
            f"Cost Basis: ${self.cost_price:.2f}",
            f"Current Price: ${self.current_price:.2f}",
            f"Market Value: ${self.market_value:.2f}",
            f"Total Change: ${self.total_change:.2f}",
            f"Gain/Loss: {self.gain_loss:.2f}%",
            f"Weekly Change: {self.weekly_change:.2f}%",
            f"PE Ratio: {self.pe_ratio}"
            ]
        return "\n".join(lines)

