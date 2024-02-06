import asyncio
import websockets
import json
# k线频道
# websocket_uri = "wss://wspap.okx.com:8443/ws/v5/business?brokerId=9999"
# subscription_message = {
#     "op": "subscribe",
#     "args": [
#         {
#             "channel": "index-candle1M",
#             "instId": "BTC-USDT"
#         }
#     ]
# }
#
# "指数行情频道"
# websocket_uri = "wss://ws.okx.com:8443/ws/v5/public"
# subscription_message = {
#     "op": "subscribe",
#     "args": [
#         {
#             "channel": "index-tickers",
#             "instId": "BTC-USDT"
#         }
#     ]
# }
async def subscribe_to_channel(uri, operation, channel, args=None):
    async with websockets.connect(uri) as websocket:
        # Construct the subscription message
        index_subscription_message = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "index-tickers",
                    "instId": "XCH-USDT"
                }
            ]
        }
        open_interest_subscription_message = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "open-interest",
                    "instId": "LTC-USD-SWAP"
                }
            ]
        }

        # Send the subscription message
        await websocket.send(json.dumps(index_subscription_message))
        await websocket.send(json.dumps(open_interest_subscription_message))

        # Listen for incoming messages
        while True:
            response = await websocket.recv()
            print(f"Received message: {response}")

# Replace "wss://ws.okx.com:8443/ws/v5/public" with your WebSocket endpoint
websocket_uri = "wss://ws.okx.com:8443/ws/v5/public"
# Replace "unsubscribe" with the desired operation, "channel" with the channel name
# and args with a list of channels to unsubscribe from
operation = "unsubscribe"
channel_name = "candle1m"
channels_to_unsubscribe = ["channel1", "channel2"]

# Run the WebSocket client
asyncio.get_event_loop().run_until_complete(
    subscribe_to_channel(websocket_uri, operation, channel_name, channels_to_unsubscribe)
)
