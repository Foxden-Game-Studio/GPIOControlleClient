let websocket;

document.getElementById("connectButton").addEventListener("click", () => {
    const serverAddressInput = document.getElementById("serverAddress").value;
    const statusElement = document.getElementById("status");

    // Validate the input (IP and optional port)
    const regex = /^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::(\d{1,5}))?$/;
    const match = serverAddressInput.match(regex);

    if (!match) {
        statusElement.textContent = "Status: Invalid address format. Use IP or IP:Port.";
        return;
    }

    // Extract IP and port from the input
    const ip = match[1];
    const port = match[2] || "8765"; // Default to port 8765 if no port is specified

    const wsUrl = `ws://${ip}:${port}`;
    console.log(`Connecting to ${wsUrl}...`);

    // Attempt to connect
    websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
        statusElement.textContent = "Status: Connected to " + wsUrl;
        console.log("WebSocket connection established!");

        // Enable disconnect button and disable connect button
        document.getElementById("disconnectButton").disabled = false;
        document.getElementById("connectButton").disabled = true;
        document.getElementById("pinInput").disabled = false;
        document.getElementById("ledOnButton").disabled = false;
        document.getElementById("ledOffButton").disabled = false;
    };

    websocket.onclose = () => {
        statusElement.textContent = "Status: Disconnected";
        console.log("WebSocket connection closed.");

        // Disable disconnect button and enable connect button
        document.getElementById("disconnectButton").disabled = true;
        document.getElementById("connectButton").disabled = false;
        document.getElementById("pinInput").disabled = true;
        document.getElementById("ledOnButton").disabled = true;
        document.getElementById("ledOffButton").disabled = true;
    };

    websocket.onerror = (error) => {
        statusElement.textContent = "Status: Connection error!";
        console.error("WebSocket error:", error);
    };

    websocket.onmessage = (event) => {
        console.log("Message from server:", event.data);
    };
});

document.getElementById("disconnectButton").addEventListener("click", () => {
    if (websocket) {
        websocket.close(); // Close the WebSocket connection
        console.log("WebSocket connection closed by user.");
    }
});

document.getElementById("ledOnButton").addEventListener("click", () => {
    ledPin = document.getElementById("pinInput").value;

    sendMessage(0, ledPin);
});

document.getElementById("ledOffButton").addEventListener("click", () => {
    ledPin = document.getElementById("pinInput").value;

    sendMessage(1, ledPin)
})


function sendMessage(functionCall, additionalInfo) {
    // Create a buffer to hold the two bytes
    const buffer = new ArrayBuffer(2); // 2 bytes

    // Create a view to write the unsigned bytes
    const view = new DataView(buffer);

    // Write the function call as the first byte (0-255 range)
    view.setUint8(0, functionCall);

    // Mask additionalInfo to keep the last 5 bits and set it as the second byte
    const infoByte = additionalInfo & 0b11111; // Keep only the last 5 bits
    view.setUint8(1, infoByte);

    // Send the message to the server
    websocket.send(buffer);
}