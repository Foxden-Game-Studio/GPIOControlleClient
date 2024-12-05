import tkinter as tk
from tkinter import messagebox
import asyncio
import websockets
import threading
import struct

class WebSocketApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WebSocket Connector")
        self.websocket = None
        
        icon = tk.PhotoImage(file='./assets/icon.png')
        self.root.iconphoto(False, icon)

        # GUI Components
        tk.Label(self.root, text="Server Address (IP:Port):").grid(row=0, column=0, padx=10, pady=5)
        self.server_address_entry = tk.Entry(self.root, width=30)
        self.server_address_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.grid(row=0, column=2, padx=10, pady=5)

        self.disconnect_button = tk.Button(self.root, text="Disconnect", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.grid(row=0, column=3, padx=10, pady=5)

        self.status_label = tk.Label(self.root, text="Status: Not connected", fg="red")
        self.status_label.grid(row=1, column=0, columnspan=4, padx=10, pady=5)

        tk.Label(self.root, text="LED Pin:").grid(row=2, column=0, padx=10, pady=5)
        self.pin_entry = tk.Entry(self.root, width=10, state=tk.DISABLED)
        self.pin_entry.grid(row=2, column=1, padx=10, pady=5)

        self.led_on_button = tk.Button(self.root, text="Turn on LED", command=lambda: self.send_message(0), state=tk.DISABLED)
        self.led_on_button.grid(row=2, column=2, padx=10, pady=5)

        self.led_off_button = tk.Button(self.root, text="Turn off LED", command=lambda: self.send_message(1), state=tk.DISABLED)
        self.led_off_button.grid(row=2, column=3, padx=10, pady=5)

        self.loop = asyncio.get_event_loop()

    def validate_address(self, address):
        import re
        regex = r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::(\d{1,5}))?$"
        match = re.match(regex, address)
        if not match:
            return None
        ip = match.group(1)
        port = match.group(2) or "8765"
        return f"ws://{ip}:{port}"

    def connect(self):
        address = self.server_address_entry.get()
        ws_url = self.validate_address(address)
        if not ws_url:
            self.status_label.config(text="Status: Invalid address format. Use IP:Port.", fg="red")
            return
        
        self.status_label.config(text=f"Connecting to {ws_url}...", fg="blue")
        threading.Thread(target=self._connect, args=(ws_url,), daemon=True).start()

    async def _connect_ws(self, ws_url):
        try:
            self.websocket = await websockets.connect(ws_url)
            self.status_label.config(text=f"Status: Connected to {ws_url}", fg="green")
            self.toggle_buttons(connected=True)
            await self.listen()
        except Exception as e:
            self.status_label.config(text=f"Status: Connection error! {str(e)}", fg="red")

    def _connect(self, ws_url):
        self.loop.run_until_complete(self._connect_ws(ws_url))

    async def listen(self):
        try:
            while self.websocket:
                message = await self.websocket.recv()
                print("Message from server:", message)
        except websockets.ConnectionClosed:
            pass
        finally:
            self.toggle_buttons(connected=False)
            self.websocket = None
            self.status_label.config(text="Status: Disconnected", fg="red")

    def disconnect(self):
        if self.websocket:
            threading.Thread(target=self._disconnect, daemon=True).start()

    async def _disconnect_ws(self):
        await self.websocket.close()
        self.websocket = None

    def disconnect(self):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self._disconnect_ws(), self.loop)
            self.status_label.config(text="Status: Disconnected", fg="red")
            self.toggle_buttons(connected=False)

    def send_message(self, function_call):
        if not self.websocket:
            messagebox.showerror("Error", "WebSocket is not connected.")
            return
        try:
            pin = int(self.pin_entry.get())
            if not (0 <= pin < 32):
                messagebox.showerror("Error", "Pin must be between 0 and 31.")
                return
            buffer = struct.pack("BB", function_call, pin & 0b11111)
            asyncio.run_coroutine_threadsafe(self.websocket.send(buffer), self.loop)
        except ValueError:
            messagebox.showerror("Error", "Invalid pin input.")

    def toggle_buttons(self, connected):
        state = tk.NORMAL if connected else tk.DISABLED
        self.disconnect_button.config(state=state)
        self.connect_button.config(state=tk.DISABLED if connected else tk.NORMAL)
        self.pin_entry.config(state=state)
        self.led_on_button.config(state=state)
        self.led_off_button.config(state=state)
        
    def getRoot(self):
        return self.root