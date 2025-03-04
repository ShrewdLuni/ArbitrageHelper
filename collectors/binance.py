import json
from collector import BaseCollector

class BinanceCollector(BaseCollector):
    def __init__(self, data_pointer):
        super().__init__("wss://stream.binance.com:9443/ws/!ticker@arr", data_pointer)

    def process_message(self, message: str):
        data = json.loads(message)
        top_pairs = [
            pair for pair in data 
            if pair['s'].endswith('USDT') and 
            float(pair['c']) > 0
        ]
        
        for ticker in top_pairs:
            symbol = ticker['s']
            price = float(ticker['c'])
            self.data_pointer[symbol]["Binance"] = price

    def subscribe(self, ws):
        pass
