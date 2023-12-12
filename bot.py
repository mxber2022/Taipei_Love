from profitview import Link, http, logger
import time

class Pr:
    VENUE = 'BitMEX'
    SYMBOL = 'LTCUSDT'

class Trading(Link):
    """See docs: https://profitview.net/docs/trading/"""

    def on_start(self):
        """Called on start up of trading script"""
        self.futures_trading_strategy()

    def futures_trading_strategy(self):
        # Set up parameters for the strategy
        short_window = 10  # Short moving average window
        long_window = 50   # Long moving average window

        while True:
            try:
                # Fetch historical candle data
                candles_data = self.fetch_candles(Pr.VENUE, sym=Pr.SYMBOL, level='1d')
				
                if 'data' in candles_data:
                    candles = candles_data['data']
					print(candles)
                    # Extract closing prices
                    closing_prices = [candle.get('close') for candle in candles]
					#print(closing_prices)
                    # Calculate moving averages
                    short_ma = sum(closing_prices[-short_window:]) / short_window
                    long_ma = sum(closing_prices[-long_window:]) / long_window
					
					print("short_ma", short_ma)
					print("long_ma", long_ma)
                    # Place trading logic here
                    if short_ma > long_ma:
                        # Bullish crossover
                        print("Bullish crossover detected. Place long trade logic here.")
      					# Example: self.place_order('buy', quantity)
						self.create_market_order(Pr.VENUE, sym=Pr.SYMBOL, side="Buy", size=1000000)

                    elif short_ma < long_ma:
                        # Bearish crossover
                        print("Bearish crossover detected. Place short trade logic here.")
						self.create_market_order(Pr.VENUE, sym=Pr.SYMBOL, side="Sell", size=1000)
                        # Example: self.place_order('sell', quantity)

                elif 'error' in candles_data:
                    error_message = candles_data['error']
                    logger.error(f"Error fetching candles: {error_message}")

            except Exception as e:
                logger.error(f"Error in strategy: {e}")
			print("done")
			self.definitely_cancel_orders()
			time.sleep(60)

    def definitely_cancel_orders(self):
		"""`cancel_order(self)` sometimes times out"""
		logger.info(f"Cancelling all orders at {Pr.VENUE} of {Pr.SYMBOL}")
		while self.cancel_order(Pr.VENUE, sym=Pr.SYMBOL)['error']:  # See https://profitview.net/docs/trading/#cancel-order
			logger.warning(f"Error cancelling orders")
			time.sleep(1)

    @http.route
    def get_route(self, data):
        """Definition of GET request endpoint - see docs for more info"""
        return data

    @http.route
    def post_route(self, data):
        """Definition of POST request endpoint - see docs for more info"""
        return data
