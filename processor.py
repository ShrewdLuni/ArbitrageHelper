import threading
import time

class DataProcessor:

    def __init__(self, data_pointer) -> None:
        self.data_pointer = data_pointer

    def process(self):
        while True:
            print("\n\n")

            for symbol in self.data_pointer:
                if len(self.data_pointer[symbol]) >= 2:
                    min_value = 99999999999999 
                    min_exchange = ""
                    max_value = -1 
                    max_exchange = ""
                    for exchange in self.data_pointer[symbol]:
                        curr = self.data_pointer[symbol][exchange]
                        if curr < min_value:
                            min_value = curr
                            min_exchange = exchange
                        if curr > max_value:
                            max_value = curr
                            max_exchange = exchange
                    if min_exchange != max_exchange:
                        print(f"BUY {symbol} at {min_exchange} for {min_value}$, SELL at {max_exchange} for {max_value}$")



#                    print(f"{symbol}: {self.data_pointer[symbol]}")
            time.sleep(1) 

    def start(self):
        thread = threading.Thread(target=self.process)
        thread.daemon = True  # Make the thread exit when the program exits
        thread.start()
        return thread

