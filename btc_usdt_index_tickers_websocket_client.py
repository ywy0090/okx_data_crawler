import websocket
import json
from datetime import datetime
import time
import os


root_path = './btc_usdt/'
# URL of the WebSocket you want to connect to
ws_url = 'wss://ws.okx.com:8443/ws/v5/public'

# Buffer for accumulating data
data_buffer = []

# File write interval in seconds (e.g., every 5 minutes)
write_interval = 120 # 2 * 60

# Subscription request to send to the server
subscribe_request = {
    "op": "subscribe",
    "args": [{
        "channel": "index-tickers",
        "instId": "BTC-USDT"
    }]
}


def on_open(ws):
    # Send the subscription request when the connection is opened
    ws.send(json.dumps(subscribe_request))


def on_error(ws, error):
    # Handle errors
    print("Error:", error)


def on_close(ws, close_status_code, close_msg):
    # Handle the closing of the connection
    print("WebSocket closed", close_status_code, close_msg)


def on_message(ws, message):
    # Process the message (assuming it's JSON)
    data = json.loads(message)

    # Append the data to the buffer
    data_buffer.append(data)

    # Check if it's time to write to the file
    current_time = time.time()
    print("cur_recv_len:" + str(current_time - on_message.last_write_time))
    if current_time - on_message.last_write_time >= write_interval:
        # Get the current date for the filename
        today_date = datetime.now().strftime('%Y-%m-%d')
        
        channel_name = data["arg"]["channel"]

        pth_name = root_path + "/" + channel_name + "/"
        
        if not os.path.exists(pth_name):
            os.makedirs(pth_name)
        
        # Create a file name based on the current date
        file_name = f"data_{today_date}.jsonl"

        # Write the buffered data to the file
        with open(pth_name+file_name, 'a') as file:
            for item in data_buffer:
                json.dump(item, file)
                file.write('\n')  # Newline for each JSON object

        # Clear the buffer after writing
        data_buffer.clear()

        # Update the last write time
        on_message.last_write_time = current_time


# Function to run the WebSocket
def run_websocket():
    on_message.last_write_time = time.time()
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
    ws.run_forever()


# Loop to keep the client running
while True:
    try:
        run_websocket()
        print("WebSocket client stopped. Attempting to restart...")
    except Exception as e:
        print("Error encountered: {}. Attempting to restart...".format(e))
    # Wait for a specified time before attempting to reconnect
    time.sleep(10)  # Adjust the sleep time as necessary
