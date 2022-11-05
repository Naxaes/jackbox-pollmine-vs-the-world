ROOM_CODE = "UKJJ"   # <--- FILL WITH 4 letter room code

import asyncio
import ssl
import websockets
import uuid
import subprocess
import sys


REQUIRED_LIBRARIES = [
    'websockets==10.4'
]

def install_libraries_with_pip(libraries):
    for library in libraries:
        subprocess.call([sys.executable, '-m', 'pip', 'install', library])


def uninstall_libraries_with_pip(libraries):
    for library in libraries:
        subprocess.call([sys.executable, '-m', 'pip', 'uninstall', library])


install_libraries_with_pip(REQUIRED_LIBRARIES)


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


async def hello(name, room_code):
    x = uuid.uuid4()
    uri = f"wss://ecast.jackboxgames.com/api/v2/audience/{room_code}/play?role=audience&name={name}&format=json&user-id={x}"
    async with websockets.connect(uri,
        subprotocols=['ecast-v0'],
        extra_headers=extra_headers
    ) as websocket:
        while True:
            response = await websocket.recv()
            print(response)


async def main():
    tasks = [asyncio.create_task(hello(f"TOM{i}", ROOM_CODE)) for i in range(10)]
    await asyncio.gather(*tasks)


asyncio.get_event_loop().run_until_complete(main())
