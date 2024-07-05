from datetime import datetime, timedelta
from collections import defaultdict
import math
from flask import Flask, request, jsonify

app = Flask(__name__)

class Stock:
    """
    A class to represent a stock.

    Attributes:
    symbol : str
        Stock symbol
    stock_type : str
        Type of stock ('Common' or 'Preferred')
    last_dividend : float
        Last dividend value in pennies
    fixed_dividend : float
        Fixed dividend percentage (for preferred stocks)
    par_value : float
        Par value of the stock in pennies
    trades : list
        List to store trades of the stock
    """

    def __init__(self, symbol, stock_type, last_dividend, fixed_dividend, par_value):
        """
        Constructs all the necessary attributes for the Stock object.

        Parameters:
        symbol : str
            Stock symbol
        stock_type : str
            Type of stock ('Common' or 'Preferred')
        last_dividend : float
            Last dividend value in pennies
        fixed_dividend : float
            Fixed dividend percentage (for preferred stocks)
        par_value : float
            Par value of the stock in pennies
        """
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = []

    def record_trade(self, timestamp, quantity, indicator, price):
        """
        Records a trade for the stock.

        Parameters:
        timestamp : datetime
            The time at which the trade occurred
        quantity : int
            Number of shares traded
        indicator : str
            Buy or sell indicator
        price : float
            Price at which the trade occurred
        """
        self.trades.append({"timestamp": timestamp, "quantity": quantity, "indicator": indicator, "price": price})

    def get_trades_in_last_5_minutes(self):
        """
        Retrieves all trades that occurred in the last 5 minutes.

        Returns:
        list: Trades from the last 5 minutes
        """
        now = datetime.now()
        return [trade for trade in self.trades if trade['timestamp'] >= now - timedelta(minutes=5)]

def calculate_dividend_yield(stock, price):
    """
    Calculates the dividend yield for a stock given its price.

    Parameters:
    stock : Stock
        The stock object
    price : float
        The price of the stock

    Returns:
    float: The dividend yield or None if price is zero
    """
    if price == 0:
        return None  # Avoid division by zero
    if stock.stock_type == "Common":
        return stock.last_dividend / price
    elif stock.stock_type == "Preferred":
        return (stock.fixed_dividend * stock.par_value) / price

def calculate_pe_ratio(stock, price):
    """
    Calculates the P/E ratio for a stock given its price.

    Parameters:
    stock : Stock
        The stock object
    price : float
        The price of the stock

    Returns:
    float: The P/E ratio or None if price or dividend is zero
    """
    if price == 0:
        return None  # Avoid division by zero
    dividend = stock.last_dividend if stock.stock_type == "Common" else stock.fixed_dividend * stock.par_value
    return price / dividend if dividend != 0 else None

def calculate_volume_weighted_stock_price(stock):
    """
    Calculates the Volume Weighted Stock Price based on trades in the past 5 minutes.

    Parameters:
    stock : Stock
        The stock object

    Returns:
    float: The volume weighted stock price
    """
    trades = stock.get_trades_in_last_5_minutes()
    total_traded_price_quantity = sum(trade['price'] * trade['quantity'] for trade in trades)
    total_quantity = sum(trade['quantity'] for trade in trades)
    return total_traded_price_quantity / total_quantity if total_quantity != 0 else 0

def calculate_gbce_all_share_index(stocks):
    """
    Calculates the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks.

    Parameters:
    stocks : list
        List of stock objects

    Returns:
    float: The GBCE All Share Index
    """
    vwsp_values = [calculate_volume_weighted_stock_price(stock) for stock in stocks]
    product = math.prod(vwsp_values)
    return product ** (1 / len(vwsp_values))

# In-memory storage for stocks
stocks = {
    "TEA": Stock("TEA", "Common", 0, 0, 100),
    "POP": Stock("POP", "Common", 8, 0, 100),
    "ALE": Stock("ALE", "Common", 23, 0, 60),
    "GIN": Stock("GIN", "Preferred", 8, 0.02, 100),
    "JOE": Stock("JOE", "Common", 13, 0, 250)
}

@app.route('/dividend_yield/<symbol>', methods=['GET'])
def get_dividend_yield(symbol):
    """
    Endpoint to get the dividend yield for a given stock symbol and price.

    URL Parameters:
    symbol (str): Stock symbol

    Query Parameters:
    price (float): Stock price

    Returns:
    json: JSON object containing the dividend yield or an error message
    """
    price = float(request.args.get('price'))
    stock = stocks.get(symbol)
    if stock:
        result = calculate_dividend_yield(stock, price)
        if result is None:
            return jsonify({"error": "Price must be greater than 0"}), 400
        return jsonify({"dividend_yield": result})
    return jsonify({"error": "Stock not found"}), 404

@app.route('/pe_ratio/<symbol>', methods=['GET'])
def get_pe_ratio(symbol):
    """
    Endpoint to get the P/E ratio for a given stock symbol and price.

    URL Parameters:
    symbol (str): Stock symbol

    Query Parameters:
    price (float): Stock price

    Returns:
    json: JSON object containing the P/E ratio or an error message
    """
    price = float(request.args.get('price'))
    stock = stocks.get(symbol)
    if stock:
        result = calculate_pe_ratio(stock, price)
        if result is None:
            return jsonify({"error": "Price and dividend must be greater than 0"}), 400
        return jsonify({"pe_ratio": result})
    return jsonify({"error": "Stock not found"}), 404

@app.route('/record_trade/<symbol>', methods=['POST'])
def record_trade(symbol):
    """
    Endpoint to record a trade for a given stock symbol.

    URL Parameters:
    symbol (str): Stock symbol

    JSON Body Parameters:
    timestamp (str): Timestamp of the trade (format: '%Y-%m-%d %H:%M:%S')
    quantity (int): Quantity of shares traded
    indicator (str): Buy or sell indicator
    price (float): Price at which the trade occurred

    Returns:
    json: JSON object containing a success message or an error message
    """
    data = request.get_json()
    stock = stocks.get(symbol)
    if stock:
        try:
            timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
            quantity = int(data['quantity'])
            indicator = data['indicator']
            price = float(data['price'])
        except (ValueError, KeyError) as e:
            return jsonify({"error": str(e)}), 400

        stock.record_trade(timestamp, quantity, indicator, price)
        return jsonify({"message": "Trade recorded successfully"})
    return jsonify({"error": "Stock not found"}), 404

@app.route('/volume_weighted_stock_price/<symbol>', methods=['GET'])
def get_volume_weighted_stock_price(symbol):
    """
    Endpoint to get the Volume Weighted Stock Price for a given stock symbol.

    URL Parameters:
    symbol (str): Stock symbol

    Returns:
    json: JSON object containing the volume weighted stock price or an error message
    """
    stock = stocks.get(symbol)
    if stock:
        result = calculate_volume_weighted_stock_price(stock)
        return jsonify({"volume_weighted_stock_price": result})
    return jsonify({"error": "Stock not found"}), 404

@app.route('/gbce_all_share_index', methods=['GET'])
def get_gbce_all_share_index():
    """
    Endpoint to get the GBCE All Share Index.

    Returns:
    json: JSON object containing the GBCE All Share Index
    """
    result = calculate_gbce_all_share_index(list(stocks.values()))
    return jsonify({"gbce_all_share_index": result})

if __name__ == '__main__':
    app.run(debug=False)
