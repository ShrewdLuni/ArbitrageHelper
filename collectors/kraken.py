import json
import requests
import websocket
import threading
from collector import BaseCollector

class KrakenCollector(BaseCollector):
    def __init__(self):
        super().__init__("wss://ws.kraken.com/v2")
        self.trading_pairs = self.get_all_pairs()

    def get_all_pairs(self):
        url = "https://api.kraken.com/0/public/AssetPairs"
        try:
            pairs = []
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for key in data["result"]:
                ws_pair = data["result"][key]["wsname"]

                if 'USD' in ws_pair.split("/"):
                    pairs.append(data["result"][key]["wsname"])
            return pairs

        except requests.RequestException as e:
            print(f"Error fetching trading pairs: {e}")
            return []

    def process_message(self, message: str):
        self.limit = 50 
        data = json.loads(message)


        if "channel" not in data:
            return
        channel = data["channel"]
        if channel == "ticker":
            result = {}
            ticker_data = data["data"][0]
            self.result[ticker_data["symbol"]] = ticker_data["last"]
            self.modulo += 1
            if self.modulo >= self.limit:
                self.modulo = 0
                print("Kraken:", self.result)
            #print(f"{ticker_data["symbol"]}: {ticker_data["last"]}$ kraken")

    def subscribe(self, ws):
        subscribe_message = json.dumps({
            "method": "subscribe",
            "params": {
                "channel": "ticker",
                "symbol": self.trading_pairs # Specify the trading pair(s)
            }
        })
        
        
        ws.send(subscribe_message)

