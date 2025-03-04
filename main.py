from collections import defaultdict
from collectors.binance import BinanceCollector
from collectors.kraken import KrakenCollector
from processor import DataProcessor


print("script runs")
data = defaultdict(dict)

binance = BinanceCollector(data)
binance.start()

kraken_collector = KrakenCollector(data)
kraken_collector.start()

data_processor = DataProcessor(data)
data_processor.start()
