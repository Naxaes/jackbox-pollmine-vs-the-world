import subprocess
import sys

DEPENDENCY = 'websockets==10.4'

print("--- INSTALLING WEBSOCKETS ----")
result = subprocess.call([sys.executable, '-m', 'pip', 'install', DEPENDENCY])

if result == -1:
    print("Couldn't install the required dependencies", file=sys.stderr)
    exit(1)

import importlib
try:
    importlib.import_module('websockets')
except ImportError:
    print("Couldn't import the required dependency. Try running it again", file=sys.stderr)
    exit(1)
finally:
    globals()['websockets'] = importlib.import_module('websockets')


import websockets
import asyncio
import ssl
import uuid

print("SUCCESS!")

ssl_context = ssl.create_default_context()

extra_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive, Upgrade",
    "DNT": "1",
    "Host": "ecast.jackboxgames.com",
    "Origin": "https://jackbox.tv",
    "Sec-Fetch-Dest": "websocket",
    "Sec-Fetch-Mode": "websocket",
    "Sec-Fetch-Site": "cross-site",
    "Sec-WebSocket-Extensions": "permessage-deflate",
    "Sec-WebSocket-Key": "bRkaILHXu0bkos9CQq7ARA==",
    "Sec-WebSocket-Protocol": "ecast-v0",
    "Sec-WebSocket-Version": "13",
    "Pragma": "no-cache",
    "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
}


async def send_request(name, room_code):
    x = uuid.uuid4()
    uri = f"wss://ecast.jackboxgames.com/api/v2/audience/{room_code}/play?role=audience&name={name}&format=json&user-id={x}"
    async with websockets.connect(uri,
        subprotocols=['ecast-v0'],
        extra_headers=extra_headers
    ) as websocket:
        while True:
            response = await websocket.recv()
            print(response)  # Uncomment to see the response.


async def main():
    room_code = input("What is your room code? ")
    print(f"Sending requests to {room_code}!")
    tasks = [asyncio.create_task(send_request(f"TED{i}", room_code)) for i in range(1000)]

    await asyncio.gather(*tasks)

asyncio.get_event_loop().run_until_complete(main())
