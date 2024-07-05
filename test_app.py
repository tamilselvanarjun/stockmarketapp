import pytest
import requests
from datetime import datetime
from app import app, stocks, calculate_dividend_yield, calculate_pe_ratio, calculate_volume_weighted_stock_price, calculate_gbce_all_share_index

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_dividend_yield(client):
    response = client.get('/dividend_yield/POP?price=100')
    assert response.status_code == 200
    assert response.json["dividend_yield"] == calculate_dividend_yield(stocks['POP'], 100)

def test_pe_ratio(client):
    response = client.get('/pe_ratio/POP?price=100')
    assert response.status_code == 200
    assert response.json["pe_ratio"] == calculate_pe_ratio(stocks['POP'], 100)

def test_record_trade(client):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    trade_data = {
        "timestamp": timestamp,
        "quantity": 10,
        "indicator": "buy",
        "price": 100
    }
    response = client.post('/record_trade/POP', json=trade_data)
    assert response.status_code == 200
    assert response.json["message"] == "Trade recorded successfully"
    # Check if trade was recorded
    trades = stocks['POP'].trades
    assert trades[-1] == {
        "timestamp": datetime.strptime(trade_data["timestamp"], '%Y-%m-%d %H:%M:%S'),
        "quantity": trade_data["quantity"],
        "indicator": trade_data["indicator"],
        "price": trade_data["price"]
    }

def test_volume_weighted_stock_price(client):
    # First, record a trade
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    trade_data = {
        "timestamp": timestamp,
        "quantity": 10,
        "indicator": "buy",
        "price": 100
    }
    client.post('/record_trade/POP', json=trade_data)
    
    response = client.get('/volume_weighted_stock_price/POP')
    assert response.status_code == 200
    assert response.json["volume_weighted_stock_price"] == calculate_volume_weighted_stock_price(stocks['POP'])

def test_gbce_all_share_index(client):
    response = client.get('/gbce_all_share_index')
    assert response.status_code == 200
    assert response.json["gbce_all_share_index"] == calculate_gbce_all_share_index(list(stocks.values()))

if __name__ == "__main__":
    pytest.main()
