import json
from collector import BaseCollector

class BinanceCollector(BaseCollector):
    def __init__(self):
        super().__init__("wss://stream.binance.com:9443/ws/!ticker@arr")

    def process_message(self, message: str):
        data = json.loads(message)
        top_pairs = [
            pair for pair in data 
            if pair['s'].endswith('USDT') and 
            float(pair['c']) > 0
        ]
        
#        print("\n--- BINANCE CRYPTO PRICES ---")
        for ticker in top_pairs:
            symbol = ticker['s']
            price = float(ticker['c'])
            self.result[symbol] = price
            self.modulo += 1
            if self.modulo >= self.limit:
                self.modulo = 0
                print("Binance:", self.result)

    def subscribe(self, ws):
        pass
