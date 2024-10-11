from ModuleIntegrated import *

address = "98:DA:60:07:3E:61"
uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"

commands = [0xf3, 0x00, 0x5A, 0x00]

pg_init()

def getKeyboardInput():
    global commands
    commands = [commands[0], 0x00, commands[2], 0x00]

    if getKey("w") and getKey('a') == False and getKey('d') == False :
        commands[0] = 0xf1
        commands[1] = 0xff
        commands[2] = 0x5a
    elif getKey('w') :
        commands[0] = 0xf1
        commands[1] = 0xff
    elif getKey("s") and getKey('a') == False and getKey('d') == False :
        commands[0] = 0xf2
        commands[1] = 0xff
        commands[2] = 0x5a
    elif getKey("s") :
        commands[0] = 0xf2
        commands[1] = 0xff
    elif getKey('w') == False and getKey('s') == False :
        commands[0] = 0xf3
        commands[1] = 0x00
    if getKey("a") :
        commands[2] = 0x00
    elif getKey("d") :
        commands[2] = 0xb4

    return commands

async def run(address):    
    client = BleakClient(address)
    await client.connect()

    os.remove('C:/linelist/testline.txt')

    outFp = None
    outCom = None
    outFp = open('C:/linelist/testline.txt', 'w')

    while True:
        await client.write_gatt_char(uuid, bytes(getKeyboardInput()))
        outCom = getKeyboardInput()
        outCom = str(outCom).replace('[', '').replace(']', '').replace(' ', '')
        outFp.writelines(outCom + '\n')
        print(getKeyboardInput())
        sleep(0.02)
        if getKey("q") :
            break
    
    outFp.close()
    print('파일에 썻읍니다.')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('Disconnected')
