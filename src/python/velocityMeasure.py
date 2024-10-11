from ModuleIntegrated import *

address = "98:DA:60:07:3E:61"
uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"

commands = [0xf3, 0x00, 0x64, 0x00]

def getKeyboardInput():
    global commands
    commands = [commands[0], 0x00, commands[2], 0x00]

    if getKey("w") and getKey('a') == False and getKey('d') == False :
        commands[0] = 0xf1
        commands[1] = 0xff
        commands[2] = 0x64
    elif getKey('w') :
        commands[0] = 0xf1
        commands[1] = 0xff
    elif getKey("s") and getKey('a') == False and getKey('d') == False :
        commands[0] = 0xf2
        commands[1] = 0xff
        commands[2] = 0x64
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

async def autDri(address):    
    client = BleakClient(address)
    await client.connect()

    pg_init()

    measurementSum = 0
    for inList in readPath() :
        measureStart = time.time()

        start = time.time()

        await client.write_gatt_char(uuid, bytes(inList))

        end = time.time()
        error = (end - start)
        sleep(0.1-error)
        measureEnd = time.time()
        measurement = measureEnd - measureStart
        measurementSum += measurement

        if getKey("q") :
            break
    if getKey('q') :
        await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
        await client.disconnect()
    await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
    print(measurementSum)
    
    pygame.quit()

async def writePath(address):   
    client = BleakClient(address)
    await client.connect()

    pg_init()
    os.remove('C:/linelist/testline.txt')

    outFp = None
    outCom = None
    outFp = open('C:/linelist/testline.txt', 'w')

    measurementSum = 0

    while True:
        measureStart = time.time()

        start = time.time()

        await client.write_gatt_char(uuid, bytes(getKeyboardInput()))
        outCom = getKeyboardInput()
        outCom = str(outCom).replace('[', '').replace(']', '').replace(' ', '')
        outFp.writelines(outCom + '\n')

        end = time.time()
        error = (end - start)
        sleep(0.1-error)

        measureEnd = time.time()
        measurement = measureEnd - measureStart
        measurementSum += measurement

        if getKey("q") :
            await client.disconnect()
            break

    outFp.close()
    print('파일에 썻읍니다.')
    print(measurementSum)
    pygame.quit()

def auEx() :
    global address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(autDri(address))
    print('disconnected')

def writeEx() :
    global address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(writePath(address))
    print('disconnected')


auEx()