from abc import ABC, abstractmethod
import websocket
import json
import threading

class BaseCollector(ABC):
    def __init__(self, ws_url: str, data_pointer):
        self.ws_url = ws_url
        self.ws = None
        self.data_pointer = data_pointer

    @abstractmethod
    def process_message(self, message: str):
        pass

    def on_message(self, ws, message):
        self.process_message(message)

    def on_error(self, ws, error):
        print(f"WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"### WebSocket Connection Closed: {close_msg} ###")

    def on_open(self, ws):
        print(f"WebSocket Connection Opened: {self.ws_url}")
        self.subscribe(ws)

    @abstractmethod
    def subscribe(self, ws):
        pass

    def run_websocket(self):
        while True:
            try:
                websocket.enableTrace(False)
                self.ws = websocket.WebSocketApp(
                    self.ws_url,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close,
                    on_open=self.on_open
                )
                self.ws.run_forever()

            except Exception as e:
                print(f"WebSocket connection error: {e}. Retrying in 5 seconds...")

    def start(self):
        thread = threading.Thread(target=self.run_websocket)
        thread.start()
        return thread
