from ModuleIntegrated import *

address = "98:DA:60:07:3E:61"
uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"

commands = [0xf3, 0x00, 0x5A, 0x00]

pg_init()

def getKeyboardInput():
    global commands
    commands = [0xf3, 0x00, commands[2], 0x00]

    if getKey("w") :
        commands[0] = 0xf1
        commands[1] = 0xff
    elif getKey("s") :
        commands[0] = 0xf2
        commands[1] = 0xff
    if getKey("a") :
        commands[2] = 0x00
    elif getKey("d") :
        commands[2] = 0xb4

    return commands

async def run(address):    
    client = BleakClient(address)
    await client.connect()

    while True:
        for inList in readPath() :
            await client.write_gatt_char(uuid, bytes(inList))
            print(inList)
            sleep(0.02)
            if getKey("q") :
                break
        if getKey('q') :
            break

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('Disconnected')