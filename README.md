# Global Beverage Corporation Exchange (GBCE) Stock Market Project

This Project provides the following functionalities:
1. Calculate the dividend yield for a given stock price.
2. Calculate the P/E ratio for a given stock price.
3. Record a trade with timestamp, quantity, buy or sell indicator, and price.
4. Calculate the Volume Weighted Stock Price based on trades in the past 5 minutes.
5. Calculate the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks.

## Endpoints

- **GET http://127.0.0.1:5000/dividend_yield/<symbol>?price=<price>**
  - Calculate the dividend yield for a given stock symbol and price.
  - URL Parameters:
    - `symbol` (str): Stock symbol
  - Query Parameters:
    - `price` (float): Stock price

- **GET http://127.0.0.1:5000/pe_ratio/<symbol>?price=<price>**
  - Calculate the P/E ratio for a given stock symbol and price.
  - URL Parameters:
    - `symbol` (str): Stock symbol
  - Query Parameters:
    - `price` (float): Stock price

- **POST http://127.0.0.1:5000/record_trade/<symbol>**
  - Record a trade with timestamp, quantity, buy or sell indicator, and price.
  - URL Parameters:
    - `symbol` (str): Stock symbol
  - JSON Body Parameters:
    - `timestamp` (str): Timestamp of the trade (format: '%Y-%m-%d %H:%M:%S')
    - `quantity` (int): Quantity of shares traded
    - `indicator` (str): Buy or sell indicator
    - `price` (float): Price at which the trade occurred

- **GET http://127.0.0.1:5000/volume_weighted_stock_price/<symbol>**
  - Calculate the Volume Weighted Stock Price based on trades in the past 5 minutes for a given stock symbol.
  - URL Parameters:
    - `symbol` (str): Stock symbol

- **GET http://127.0.0.1:5000/gbce_all_share_index**
  - Calculate the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks.

## To Run the Application

### Using Python

1. Save the main application file as `app.py`.
2. Install Flask:
    ```bash
    pip install flask
    ```
3. Run the application:
    ```bash
    python app.py
    ```
4. Use an API client like Postman or your web browser to interact with the API endpoints.

### Using Docker

1. Ensure you have Docker and Docker Compose installed.
2. Build the Docker image:
    ```bash
    docker-compose build
    ```
3. Run the Docker containers:
    ```bash
    docker-compose up
    ```
4. The application will be available at `http://127.0.0.1:5000`. Use an API client like Postman or your web browser to interact with the API endpoints.

## Testing

1. Save the test code as `test_app.py` in the same directory as `app.py`.
2. Install pytest:
    ```bash
    pip install pytest
    ```
3. Run the tests:
    ```bash
    pytest test_app.py
    ```

### Testing with Docker

1. Ensure you have Docker and Docker Compose installed.
2. Build the Docker image (if not already built):
    ```bash
    docker-compose build
    ```
3. Run the Docker containers:
    ```bash
    docker-compose up
    ```
