from ModuleIntegrated import *

address = "98:DA:60:07:3E:61"
uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"

commands = [0xf3, 0x00, 0x64, 0x00]

Qualification = False
outCode = True
connCode = False

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

async def dirDri(address):   
    global connCode
    client = BleakClient(address)
    await client.connect()

    connCode = True
    state()

    pg_init()
    while True:
        await client.write_gatt_char(uuid, bytes(getKeyboardInput()))
        print(getKeyboardInput())
        sleep(0.1)
        if getKey("q") :
            await client.disconnect()
            break
    pygame.quit()

    connCode = False
    state()

async def autDri(address): 
    global connCode   
    client = BleakClient(address)
    await client.connect()

    connCode = True
    state()

    pg_init()
    while True:
        for inList in readPath() :
            start = time.time()

            await client.write_gatt_char(uuid, bytes(inList))

            end = time.time()
            error = (end - start)
            sleep(0.1-error)

            if getKey("q") :
                break
        if getKey('q') :
            await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
            await client.disconnect()
            break
    pygame.quit()

    connCode = False
    state()

async def writePath(address):   
    global connCode
    client = BleakClient(address)
    await client.connect()

    connCode = True
    state()

    pg_init()
    os.remove('C:/linelist/testline.txt')

    outFp = None
    outCom = None
    outFp = open('C:/linelist/testline.txt', 'w')

    while True:
        start = time.time()

        await client.write_gatt_char(uuid, bytes(getKeyboardInput()))
        outCom = getKeyboardInput()
        outCom = str(outCom).replace('[', '').replace(']', '').replace(' ', '')
        outFp.writelines(outCom + '\n')

        end = time.time()
        error = (end - start)
        sleep(0.1-error)

        if getKey("q") :
            await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
            await client.disconnect()
            break
    outFp.close()
    print('파일에 썻읍니다.')
    pygame.quit()

    connCode = False
    state()

def chkData() :
    global Qualification

    if id.get() == '1234' and pw.get() == '4321' :
        messagebox.showinfo('알림', '로그인떵공')
        login.destroy()
        Qualification = True
    else :
        messagebox.showerror('경고', '로그인띨패')

def dirEx() :
    stateLbl.configure(text = '연결 상테 : Connecting...')
    main.update()

    global address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dirDri(address))
    print('disconnected')

def auEx() :
    stateLbl.configure(text = '연결 상테 : Connecting...')
    main.update()

    global address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(autDri(address))
    print('disconnected')

def writeEx() :
    stateLbl.configure(text = '연결 상테 : Connecting...')
    main.update()

    global address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(writePath(address))
    print('disconnected')

login = Tk()
login.title('로그인')
login.geometry('250x80')
login.resizable(width = FALSE, height = FALSE)

id, pw = StringVar(), StringVar()
lb1 = Label(login, text = 'ID').place(x = 0, y = 0)
lb2 = Label(login, text = 'PW').place(x = 0, y = 20)
ent1 = Entry(login, textvariable = id).place(x = 60, y = 0)
ent2 = Entry(login, textvariable = pw, show = '*').place(x = 60, y = 20)
btn = Button(login, text = '확인', command = chkData, width = 10, height = 1).place(x = 110, y = 45)

login.mainloop()

while True :
    if Qualification and outCode :
        main = Tk()
        break
    elif outCode :
        break

main.title('차랑재어')
main.geometry('1024x768')
main.resizable(width = FALSE, height = FALSE)

def state() :
    global connCode

    if connCode :
        stateLbl.configure(text = '연결 상테 : Connected')
    else :
        stateLbl.configure(text = '연결 상테 : Disconnected')
    main.update()

stateLbl = Label(main, text = '연결 상테 : Disconnected', font = 'default 20')
dirbtn = Button(main, text = '직접재어', font = 'default 25', command = dirEx, width = 10, height = 4).place(x = 70, y = 70)
autbtn = Button(main, text = '경로주헹모드', font = 'default 25', command = auEx, width = 10, height = 4).place(x = 70, y = 300)
writeLinebtn = Button(main, text = '경로 입력', font = 'default 25', command = writeEx, width = 10, height = 4).place(x = 70, y = 530)
stateLbl.place(x = 600, y = 70)

main.mainloop()