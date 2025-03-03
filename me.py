import requests
import time
from datetime import datetime
import json
from pathlib import Path

class BinanceListingMonitor:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"
        self.cache_file = Path("known_symbols.json")
        self.known_symbols = self.load_known_symbols()

    def load_known_symbols(self):
        """Load previously seen symbols from cache file"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return set(json.load(f))
        return set()

    def save_known_symbols(self):
        """Save current symbols to cache file"""
        with open(self.cache_file, 'w') as f:
            json.dump(list(self.known_symbols), f)

    def get_exchange_info(self):
        """Fetch current exchange information from Binance"""
        try:
            response = requests.get(f"{self.base_url}/exchangeInfo")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange info: {e}")
            return None

    def send_notification(self, symbol, details):
        """Send notification about new listing"""
        # Print notification (you can modify this to use other notification methods)
        print("\n" + "="*50)
        print(f"NEW LISTING DETECTED: {symbol}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Quote Asset: {details['quoteAsset']}")
        print(f"Base Asset: {details['baseAsset']}")
        print(f"Status: {details['status']}")
        print("="*50 + "\n")

        # You could add additional notification methods here:
        # - Email notifications
        # - Desktop notifications
        # - Telegram bot messages
        # - Discord webhooks
        # - SMS notifications

    def monitor_listings(self, interval=60):
        """
        Monitor for new listings continuously
        
        Args:
            interval (int): Seconds to wait between checks
        """
        print(f"Starting Binance listing monitor... Checking every {interval} seconds")
        
        while True:
            try:
                # Get current exchange information
                exchange_info = self.get_exchange_info()
                
                if exchange_info:
                    # Check each symbol
                    current_symbols = set()
                    for symbol_info in exchange_info['symbols']:
                        symbol = symbol_info['symbol']
                        current_symbols.add(symbol)
                        
                        # If this is a new symbol we haven't seen before
                        if symbol not in self.known_symbols:
                            self.send_notification(symbol, symbol_info)
                            self.known_symbols.add(symbol)
                    
                    # Update cache file
                    self.save_known_symbols()
                
                # Wait for next check
                time.sleep(interval)
                
            except Exception as e:
                print(f"Error in monitor loop: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    monitor = BinanceListingMonitor()
    monitor.monitor_listings()