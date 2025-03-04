from collectors.binance import BinanceCollector
from collectors.kraken import KrakenCollector 


print("script runs")
binance = BinanceCollector()
binance.start()

kraken_collector = KrakenCollector()
kraken_collector.start()
