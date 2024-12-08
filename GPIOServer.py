import tkinter as tk
import asyncio
from uiComponents import UIComponents
from webSocketManager import WebSocketManager
from helpers import validate_address

class GPIOServerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WebSocket Connector")
        self.websocket_manager = WebSocketManager(self.update_status, self.show_frame)
        self.root.geometry("600x200")

        icon = tk.PhotoImage(file='./assets/icon.png')
        self.root.iconphoto(False, icon)

        self.connection_frame = tk.Frame(self.root)
        self.led_control_frame = tk.Frame(self.root)
        self.selectFame = tk.Frame(self.root)
        self.distanceSensorFrame = tk.Frame(self.root)

        self.server_address_entry, self.connect_button, self.status_label = UIComponents.createSonnectionScreen(
            self.connection_frame, self.connect
        )
        self.pin_entry, self.led_on_button, self.led_off_button, self.disconnect_button = UIComponents.createLEDControlScreen(
            self.led_control_frame, self.send_message, self.disconnect
        )
        self.selectLED, self.selectDistanceSensor = UIComponents.createObjSelectScreen(
            self.selectFame, self.show_frame
        )
        self.sonsorIdEntry, self.trigPinEntry, self.echoPinEntry, self.startMButton, self.stopMButton = UIComponents.createDistanceSensorScreen(
            self.distanceSensorFrame, self.send_message, None
        )

        self.show_frame("connection")

    def show_frame(self, frame_name):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        if frame_name == "connection":
            self.connection_frame.pack(fill=tk.BOTH, expand=True)
        elif frame_name == "led":
            self.led_control_frame.pack(fill=tk.BOTH, expand=True)
        elif frame_name == "select":
            self.selectFame.pack(fill=tk.BOTH, expand=True)
        elif frame_name == "distanceSensor":
            self.distanceSensorFrame.pack(fill=tk.BOTH, expand=True)

    def update_status(self, text, color):
        self.status_label.config(text=f"Status: {text}", fg=color)

    def connect(self):
        address = self.server_address_entry.get()
        ws_url = validate_address(address)
        if not ws_url:
            self.update_status("Invalid address format. Use IP:Port.", "red")
            return
        self.update_status(f"Connecting to {ws_url}...", "blue")
        asyncio.run_coroutine_threadsafe(self.websocket_manager.connect(ws_url), self.websocket_manager.loop)

    def disconnect(self):
        asyncio.run_coroutine_threadsafe(self.websocket_manager.disconnect(), self.websocket_manager.loop)

    def send_message(self, function_call):
        try:
            ID = int(self.sonsorIdEntry.get())
            pin0 = int(self.trigPinEntry.get())
            pin1 = int(self.echoPinEntry.get())
            
            if not (0 <= pin0 < 32):
                raise ValueError("Pin must be between 0 and 31.")
            if not (0 <= pin1 < 32):
                raise ValueError("Pin must be between 0 and 31.")
            
            self.websocket_manager.send_message(function_call, ID, pin0, pin1)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
            
    def getRoot(self):
        return self.root
