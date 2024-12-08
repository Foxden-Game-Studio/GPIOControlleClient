import asyncio
import websockets
import struct
import threading

class WebSocketManager:
    def __init__(self, update_status_callback, show_frame_callback):
        self.websocket = None
        self.loop = asyncio.new_event_loop()
        self.update_status = update_status_callback
        self.show_frame = show_frame_callback
        asyncio.set_event_loop(self.loop)
        threading.Thread(target=self.start_event_loop, daemon=True).start()

    def start_event_loop(self):
        self.loop.run_forever()

    async def connect(self, ws_url):
        try:
            self.websocket = await websockets.connect(ws_url)
            self.update_status(f"Connected to {ws_url}", "green")
            self.show_frame("select")
            await self.listen()
        except Exception as e:
            self.update_status(f"Connection error: {e}", "red")

    async def listen(self):
        try:
            while self.websocket:
                message = await self.websocket.recv()
                print("Message from server:", message)
        except websockets.ConnectionClosed:
            pass
        finally:
            self.websocket = None
            self.update_status("Disconnected", "red")
            self.show_frame("connection")

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    def send_message(self, function_call, ID, pin0, pin1):
        if not self.websocket:
            raise RuntimeError("WebSocket is not connected.")
        buffer = struct.pack("BBBB", function_call, ID, pin0, pin1)
        asyncio.run_coroutine_threadsafe(self.websocket.send(buffer), self.loop)
