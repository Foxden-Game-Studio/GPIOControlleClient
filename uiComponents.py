import tkinter as tk
from tkinter import messagebox

class UIComponents:
    @staticmethod
    def createSonnectionScreen(connection_frame, connect_callback):
        tk.Label(connection_frame, text="Server Address (IP:Port):").grid(row=0, column=0, padx=10, pady=5)
        server_address_entry = tk.Entry(connection_frame, width=30)
        server_address_entry.grid(row=0, column=1, padx=10, pady=5)
        
        connect_button = tk.Button(connection_frame, text="Connect", command=connect_callback)
        connect_button.grid(row=0, column=2, padx=10, pady=5)
        
        status_label = tk.Label(connection_frame, text="Status: Not connected", fg="red")
        status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        return server_address_entry, connect_button, status_label
    
    @staticmethod
    def createObjSelectScreen(objSelectFrame, selectionCallback):
        tk.Label(objSelectFrame, text="Select a Component:").grid(row=0, column=0, padx=10, pady=5)
        
        selectLED = tk.Button(objSelectFrame, text="LED", command=lambda: selectionCallback("led"))
        selectLED.grid(row=1, column=0, padx=10, pady=5)
        
        selectDistaceSensor = tk.Button(objSelectFrame, text="Distance Sensor", command=lambda: selectionCallback("distanceSensor"))
        selectDistaceSensor.grid(row=2, column=0, padx=10, pady=5)
        
        return selectLED, selectDistaceSensor

    @staticmethod
    def createLEDControlScreen(led_control_frame, send_message_callback, disconnect_callback):
        tk.Label(led_control_frame, text="LED Pin:").grid(row=0, column=0, padx=10, pady=5)
        pin_entry = tk.Entry(led_control_frame, width=10)
        pin_entry.grid(row=0, column=1, padx=10, pady=5)

        led_on_button = tk.Button(led_control_frame, text="Turn on LED", command=lambda: send_message_callback(0))
        led_on_button.grid(row=0, column=2, padx=10, pady=5)

        led_off_button = tk.Button(led_control_frame, text="Turn off LED", command=lambda: send_message_callback(1))
        led_off_button.grid(row=0, column=3, padx=10, pady=5)

        disconnect_button = tk.Button(led_control_frame, text="Disconnect", command=disconnect_callback)
        disconnect_button.grid(row=1, column=0, columnspan=4, pady=10)

        return pin_entry, led_on_button, led_off_button, disconnect_button
    
    @staticmethod
    def createDistanceSensorScreen(distanceSensorFrame, initCallback, checkDistanceCallback):
        tk.Label(distanceSensorFrame, text="Distance Sensor").grid(row=0, column=0, padx=10, pady=5)
        
        tk.Label(distanceSensorFrame, text="Sensor ID:").grid(row=1, column=0, padx=10, pady=5)
        sensorIdEntry = tk.Entry(distanceSensorFrame, width=10)
        sensorIdEntry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(distanceSensorFrame, text="Trigger Pin:").grid(row=2, column=0, padx=10, pady=5)
        trigPinEntry = tk.Entry(distanceSensorFrame, width=10)
        trigPinEntry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(distanceSensorFrame, text="Echo Pin:").grid(row=3, column=0, padx=10, pady=5)
        echoPinEntry = tk.Entry(distanceSensorFrame, width=10)
        echoPinEntry.grid(row=3, column=1, padx=10, pady=5)
        
        initButton = tk.Button(distanceSensorFrame, text="Init Distance Sensor", command=lambda: initCallback(2))
        initButton.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(distanceSensorFrame, text="Measurement:").grid(row=0, column=3, padx=10, pady=5)
        startMButton = tk.Button(distanceSensorFrame, text="start Distace Measurement")
        startMButton.grid(row=1, column=4, padx=10, pady=5)
        
        stopMButton = tk.Button(distanceSensorFrame, text="stop Distance Measurement")
        stopMButton.grid(row=2, column=4, padx=10, pady=5)
        
        return sensorIdEntry, trigPinEntry, echoPinEntry, startMButton, stopMButton
