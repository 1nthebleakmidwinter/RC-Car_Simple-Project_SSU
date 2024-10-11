import asyncio
from bleak import BleakClient
import time


address = "98:DA:60:07:3E:61"

uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
uuid2 = '0000ffe1-0000-1000-8000-00805f9b34fb'


async def run(address):  
    client = BleakClient(address)
    await client.connect()
    print('connected')
    while True :   
        read_data = await client.read_gatt_char(uuid2)
        print(read_data)
        d = read_data.decode().replace('\x00', '')
        print(int(d))


print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')