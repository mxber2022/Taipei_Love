# crypto derivatives trading bot - BitMEX

### Overview
The trading bot is designed to implement a basic moving average crossover strategy for futures trading on the BitMEX exchange with the LTCUSDT trading pair. The algorithm uses the ProfitView library for interacting with the exchange and executing trades.

Requirements
* Python 3.6
* ProfitView library 

## Warning

### Valid Market Conditions:

1. Trending Markets:

The algorithm is designed to perform well in trending markets where a sustained directional movement is observed.
Bullish crossovers (short MA > long MA) may be effective during upward trends.
Bearish crossovers (short MA < long MA) may be effective during downward trends.

2. Stable Price Movements:

The strategy assumes that the market is characterized by relatively stable price movements over the short and long windows used for moving average calculations.

3. Smooth Price Trends:

The algorithm is suited for markets with smooth and well-defined trends, where crossovers are more likely to indicate significant changes in market direction.

4. Volatility within Tolerable Range:

Moderate volatility is often favorable. Extreme volatility could lead to false signals or rapid changes in trend direction.

### Challenging Market Conditions:

1. Sideways or Range-Bound Markets:

In sideways or range-bound markets with no clear trend, the moving average crossover strategy may generate false signals, resulting in unprofitable trades.

2. Whipsawing:

Whipsawing can occur when the market experiences frequent, short-lived price fluctuations, leading to multiple crossovers without a clear trend direction.

3. Abrupt Price Changes:

Rapid and unpredictable price changes can lead to delayed responses by the algorithm, potentially resulting in losses.

### 1. Initialization and Setup

The bot is a Python script that uses the ProfitView library for trading operations. It starts by importing necessary modules and defining a class called `Trading` that inherits from `Link`, a class provided by ProfitView.

```python
from profitview import Link, http, logger
import time
```

### 2. Trading Class Initialization

The `Trading` class is defined, inheriting from `Link`. This class will contain the trading logic and strategies.

```python
class Trading(Link):
    def on_start(self):
        self.futures_trading_strategy()
```

The `on_start` method is called when the trading script is initialized. In this case, it immediately calls the `futures_trading_strategy` method.

### 3. Futures Trading Strategy

The `futures_trading_strategy` method is the core of the trading algorithm. It implements a basic moving average crossover strategy.

```python
def futures_trading_strategy(self):
    short_window = 10
    long_window = 50

    while True:
        try:
            candles_data = self.fetch_candles(Pr.VENUE, sym=Pr.SYMBOL, level='1d')
            
            if 'data' in candles_data:
                candles = candles_data['data']
                closing_prices = [candle.get('close') for candle in candles]

                short_ma = sum(closing_prices[-short_window:]) / short_window
                long_ma = sum(closing_prices[-long_window:]) / long_window

                if short_ma > long_ma:
                    # Bullish crossover
                    self.create_market_order(Pr.VENUE, sym=Pr.SYMBOL, side="Buy", size=1000000)

                elif short_ma < long_ma:
                    # Bearish crossover
                    self.create_market_order(Pr.VENUE, sym=Pr.SYMBOL, side="Sell", size=1000)

            elif 'error' in candles_data:
                error_message = candles_data['error']
                logger.error(f"Error fetching candles: {error_message}")

        except Exception as e:
            logger.error(f"Error in strategy: {e}")
            self.definitely_cancel_orders()
            time.sleep(60)
```

### 4. Moving Average Crossover Strategy

The moving average crossover strategy involves calculating short and long moving averages and making trading decisions based on their relationship.

- **Short MA Calculation:**
  ```python
  short_ma = sum(closing_prices[-short_window:]) / short_window
  ```

- **Long MA Calculation:**
  ```python
  long_ma = sum(closing_prices[-long_window:]) / long_window
  ```

### 5. Trading Logic

The trading logic is implemented based on the relationship between the short and long moving averages.

- **Bullish Crossover:**
  ```python
  if short_ma > long_ma:
      # Bullish crossover
      self.create_market_order(Pr.VENUE, sym=Pr.SYMBOL, side="Buy", size=1000000)
  ```

- **Bearish Crossover:**
  ```python
  elif short_ma < long_ma:
      # Bearish crossover
      self.create_market_order(Pr.VENUE, sym=Pr.SYMBOL, side="Sell", size=1000)
  ```

### 6. Error Handling

The code includes error handling for cases where fetching candles fails or encounters an error. Error messages are logged for debugging.

### 7. Order Cancellation

The `definitely_cancel_orders` method is responsible for canceling orders. It attempts to cancel orders until successful, addressing potential timeouts.

```python
def definitely_cancel_orders(self):
    logger.info(f"Cancelling all orders at {Pr.VENUE} of {Pr.SYMBOL}")
    while self.cancel_order(Pr.VENUE, sym=Pr.SYMBOL)['error']:
        logger.warning(f"Error cancelling orders")
        time.sleep(1)
```

### 8. HTTP Routes

The bot also includes two HTTP routes (`get_route` and `post_route`) for handling GET and POST requests, respectively. These routes simply return the received data.

```python
@http.route
def get_route(self, data):
    return data

@http.route
def post_route(self, data):
    return data
```

### 9. Continual Execution

The entire algorithm runs in a continuous loop (`while True`), fetching candle data, applying the trading strategy, handling errors, and canceling orders. It then sleeps for 60 seconds before repeating the process.

```python
while True:
    # Trading logic
    # Error handling
    # Order cancellation
    time.sleep(60)
```

This loop ensures that the trading strategy is applied repeatedly over time. The bot's behavior can be adjusted by modifying parameters, such as moving average windows or order sizes, to suit specific trading preferences.




