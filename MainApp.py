from ModuleIntegrated import *

address = "98:DA:60:07:3E:61"
uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
uuid2 = '0000ffe1-0000-1000-8000-00805f9b34fb'

commands = [0xf3, 0x00, 0x64, 0x00]

Qualification = False
outCode = True
connCode = 0
mode = ''
posCode = 0

speed = 67
phase = 90
delta_phase = 22.3

background = pygame.image.load('C:/controller/posbg.png')
car = pygame.image.load('C:/controller/car.png')
car = pygame.transform.scale(car, (25, 25))
car_size = car.get_rect().size
car_width = car_size[0]
car_height = car_size[1]
car_x_pos = 75 - (car_width/2)
car_y_pos = 700 - car_height

right_center_x = car_x_pos + 5*speed*math.sqrt(3)/3
right_center_y = car_y_pos + 5*speed/3
left_center_x = car_x_pos - 5*speed*math.sqrt(3)/3
left_center_y = car_y_pos + 5*speed/3

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

async def car_connect(address):
    global mode
    global connCode
    global client
    if connCode == 0 or connCode == 2 :
        try :
            client = BleakClient(address)
            await client.connect()

            connCode = 1
            connbtn.configure(text = '연결 해제')
            state()

        except bleak.exc.BleakDeviceNotFoundError :
            connCode = 0
            state()
            messagebox.showerror('경고', '차량을 찾을 수 없습니다.')

    elif connCode == 1 or connCode == 3 :
        await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
        await client.disconnect()
        connCode = 0
        connbtn.configure(text = '차량 연결')
        mode = 'zero'
        state()
        modeState()

async def dirDri():  
    global mode 
    modeState()
    while True:
        if mode == 'zero' :
            break

        await client.write_gatt_char(uuid, bytes(getKeyboardInput()))
        positioningUpdate(getKeyboardInput())
        kineticState(getKeyboardInput())

        sleep(0.25)
        if getKey("o") :
            await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
            break
    await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
    mode = 'zero'
    modeState()

async def autDri(): 
    global mode
    modeState()

    while True:
        for inList in readPath() :
            if mode == 'zero' :
                break

            start = time.time()

            await client.write_gatt_char(uuid, bytes(inList))
            positioningUpdate(inList)
            kineticState(inList)

            end = time.time()
            error = (end - start)
            sleep(0.3-error)

            if getKey("o") :
                await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
                break
        if getKey('o') :
            break
        if mode == 'zero' :
            break
    await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
    mode = 'zero'
    modeState()

async def writePath():  
    global mode
    modeState()
    os.remove('C:/linelist/testline.txt')

    outFp = None
    outCom = None
    outFp = open('C:/linelist/testline.txt', 'w')

    while True:
        if mode == 'zero' :
            break

        start = time.time()

        await client.write_gatt_char(uuid, bytes(getKeyboardInput()))
        positioningUpdate(getKeyboardInput())
        kineticState(getKeyboardInput())

        outCom = getKeyboardInput()
        outCom = str(outCom).replace('[', '').replace(']', '').replace(' ', '')
        outFp.writelines(outCom + '\n')

        end = time.time()
        error = (end - start)
        sleep(0.3-error)

        if getKey("o") :
            await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
            break
    await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))
    outFp.close()
    print('파일에 썻읍니다.')
    mode = 'zero'
    modeState()

async def forcedBack() :
    await client.write_gatt_char(uuid, bytes([0xf2, 0x00, 0x64, 0x00]))
    sleep(0.3)
    await client.write_gatt_char(uuid, bytes([0xf3, 0x00, 0x64, 0x00]))

def chkData() :
    global Qualification

    if id.get() == '1234' and pw.get() == '4321' :
        messagebox.showinfo('알림', '로그인 성공')
        login.destroy()
        Qualification = True
    else :
        messagebox.showerror('경고', '로그인 실패')

def connEx() :
    global address
    global connCode

    if connCode == 0 :
        connCode = 2
        state()

    elif connCode == 1 :
        connCode = 3
        state()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(car_connect(address))

async def dirmain() :
    await asyncio.gather(emergencyCHK(), dirDri())

def dirEx() :
    global mode
    mode = 'direct'
    asyncio.run(dirmain())

async def aumain() :
    await asyncio.gather(emergencyCHK(), autDri())

def auEx() :
    global mode
    mode = 'auto'
    asyncio.run(aumain())

async def writemain() :
    await asyncio.gather(emergencyCHK(), writePath())

def writeEx() :
    global mode
    mode = 'input'
    asyncio.run(writemain())

async def backmain() :
    await asyncio.gather(forcedBack())

def backEx() :
    asyncio.run(backmain())

login = tk.Tk()
loginLogo = tk.PhotoImage(file = 'C:/controller/loginlogo.png')
loginBG = tk.PhotoImage(file = 'C:/controller/loginbg.png')
login.wm_iconphoto(False, loginLogo)
login.title('차량 제어 - 로그인')
login.geometry('512x384')
login.resizable(width = tk.FALSE, height = tk.FALSE)

id, pw = tk.StringVar(), tk.StringVar()
loginbg = tk.Label(login, image = loginBG).place(x = -250, y = -100)
lb1 = tk.Label(login, text = 'ID', fg = 'white', bg = '#003377').place(x = 130, y = 242)
lb2 = tk.Label(login, text = 'PW', fg = 'white', bg = '#003377').place(x = 130, y = 282)
lb3 = tk.Label(login, text = 'Controller LOCKED', font = 'default 23', fg = 'white', bg = '#003377').place(x = 120, y = 35)
ent1 = tk.Entry(login, textvariable = id).place(x = 160, y = 240, width = 200, height = 25)
ent2 = tk.Entry(login, textvariable = pw, show = '*').place(x = 160, y = 280, width = 200, height = 25)
btn = tk.Button(login, text = '확인', command = chkData, width = 10, height = 1).place(x = 220, y = 320)

login.mainloop()

while True :
    if Qualification and outCode :
        main = tk.Tk()
        break
    elif outCode :
        break

appLogo = tk.PhotoImage(file = 'C:/controller/applogo.png')
main.wm_iconphoto(False, appLogo)
main.title('차량 제어')
main.geometry('1024x768')
main.resizable(width = tk.FALSE, height = tk.FALSE)

def state() :
    global connCode

    if connCode == 1 :
        stateLbl.configure(text = '연결 상태 : Connected')
    elif connCode == 0 :
        stateLbl.configure(text = '연결 상태 : Disconnected')
    elif connCode == 2 :
        stateLbl.configure(text = '연결 상태 : Connecting...')
    elif connCode == 3 :
        stateLbl.configure(text = '연결 상태 : Disconnecting...')
    main.update()

def modeState() :
    global mode

    if mode == 'direct' :
        modeLbl.configure(text = '현재 모드 : 직접 제어')
    elif mode == 'auto' :
        modeLbl.configure(text = '현재 모드 : 경로 주행')
    elif mode == 'input' :
        modeLbl.configure(text = '현재 모드 : 경로 입력')
    elif mode == 'zero' :
        modeLbl.configure(text = '현재 모드 : 공회전')
        kineticState([0xf3, 0x00, 0x64, 0x00])
    main.update()

def positioningSystem() :
    global posCode, pos, car_x_pos, car_y_pos, background

    if posCode == 0 :
        posCode = 1
        posbtn.configure(text = 'Positioning Off')
        main.update()

        pos = pg_init()

        pos.blit(background, (-25, -25))
        pos.blit(car, (car_x_pos, car_y_pos))
        pygame.display.update()
            
    else :
        posCode = 0
        posbtn.configure(text = 'Positioning On')
        main.update()
        pygame.quit()

def positioningUpdate(commands) :
    global pos, car_x_pos, car_y_pos, car_width, car_height, background
    global speed, phase, delta_phase, right_center_x, right_center_y
    global left_center_x, left_center_y

    if commands[0] == 0xf3 :
        car_x_pos += 0
        car_y_pos += 0
    elif commands[0] == 0xf1 and commands[2] == 0x64 :
        car_x_pos += speed * cos(phase)
        car_y_pos += -(speed * sin(phase))
        right_center_x += speed * cos(phase)
        right_center_y += -(speed * sin(phase))
        left_center_x += speed * cos(phase)
        left_center_y += -(speed * sin(phase))
    elif commands[0] == 0xf2 and commands[2] == 0x64 :
        car_x_pos += -(speed * cos(phase))
        car_y_pos += speed * sin(phase)
        right_center_x += -(speed * cos(phase))
        right_center_y += speed * sin(phase)
        left_center_x += -(speed * cos(phase))
        left_center_y += speed * sin(phase)
    elif commands[0] == 0xf1 and commands[2] == 0x00 :
        phase += delta_phase*(7/6)
        car_x_pos = (10*speed * cos(phase-60)/3) + left_center_x
        car_y_pos = -(10*speed * sin(phase-60)/3) + left_center_y
        right_center_x = (10*speed*math.sqrt(3) * cos(phase-90)/3) + left_center_x
        right_center_y = -(10*speed*math.sqrt(3) * sin(phase-90)/3) + left_center_y
    elif commands[0] == 0xf1 and commands[2] == 0xb4 :
        phase -= delta_phase
        car_x_pos = (10*speed * cos(phase+60)/3) + right_center_x
        car_y_pos = -(10*speed * sin(phase+60)/3) + right_center_y
        left_center_x = (10*speed*math.sqrt(3) * cos(phase+90)/3) + right_center_x
        left_center_y = -(10*speed*math.sqrt(3) * sin(phase+90)/3) + right_center_y
    elif commands[0] == 0xf2 and commands[2] == 0x00 :
        phase -= delta_phase*(7/6)
        car_x_pos = (10*speed * cos(phase-60)/3) + left_center_x
        car_y_pos = -(10*speed * sin(phase-60)/3) + left_center_y
        right_center_x = (10*speed*math.sqrt(3) * cos(phase-90)/3) + left_center_x
        right_center_y = -(10*speed*math.sqrt(3) * sin(phase-90)/3) + left_center_y
    elif commands[0] == 0xf2 and commands[2] == 0xb4 :
        phase += delta_phase
        car_x_pos = (10*speed * cos(phase+60)/3) + right_center_x
        car_y_pos = -(10*speed * sin(phase+60)/3) + right_center_y
        left_center_x = (10*speed*math.sqrt(3) * cos(phase+90)/3) + right_center_x
        left_center_y = -(10*speed*math.sqrt(3) * sin(phase+90)/3) + right_center_y

    if car_x_pos < 0 :
        car_x_pos = 0
    elif car_x_pos > 600 - car_width :
        car_x_pos = 600 - car_width
    if car_y_pos < 0 :
        car_y_pos = 0
    elif car_y_pos > 800 - car_height :
        car_y_pos = 800 - car_height

    phase = phase % 360
    pos.blit(background, (-25, -25))
    pos.blit(car, (car_x_pos, car_y_pos))
    car_update()
    carposCHK()
    pygame.display.update()

def positionInit() :
    global pos, car_x_pos, car_y_pos, phase
    global right_center_x, right_center_y, left_center_x, left_center_y

    phase = 90
    car_x_pos = 75 - (car_width/2)
    car_y_pos = 700 - car_height
    right_center_x = car_x_pos + 5*speed*math.sqrt(3)/3
    right_center_y = car_y_pos + 5*speed/3
    left_center_x = car_x_pos - 5*speed*math.sqrt(3)/3
    left_center_y = car_y_pos + 5*speed/3

    pos.blit(background, (-25, -25))
    pos.blit(car, (car_x_pos, car_y_pos))
    car_update()
    pygame.display.update()

r = 0.55

appBG = Image.open('C:/controller/appbackground.png')
appBG = ImageTk.PhotoImage(appBG)

carBG = Image.open('C:/controller/carbg.png')
carimg = Image.open('C:/controller/car_upside.png')
carimgSize = carimg.size
carimg = carimg.resize((int(carimgSize[0]*(0.5)), int(carimgSize[1]*(0.5))))
carimg = carimg.rotate(phase-150, expand = 1)
carBG.paste(carimg, (175, 175), carimg)
carBGsize = carBG.size
carBG = carBG.resize((int(carBGsize[0]*r), int(carBGsize[1]*r)))

carimg = ImageTk.PhotoImage(carBG)

def car_update() :
    global phase, r
    carBG = Image.open('C:/controller/carbg.png')
    carimg = Image.open('C:/controller/car_upside.png')
    carimgSize = carimg.size
    carimg = carimg.resize((int(carimgSize[0]*(0.5)), int(carimgSize[1]*(0.5))))
    carimg = carimg.rotate(phase-150, expand = 1)
    carBG.paste(carimg, (175, 175), carimg)
    carBGsize = carBG.size
    carBG = carBG.resize((int(carBGsize[0]*r), int(carBGsize[1]*r)))
    carimg = ImageTk.PhotoImage(carBG)
    
    carImg.configure(image = carimg)
    carImg.image = carimg

def kineticState(commands) :
    if commands[0] == 0xf3 and commands[2] == 0x64 :
        kineticLbl.configure(text = '주행 상태 : 정지')
    elif commands[0] == 0xf3 and commands[2] == 0x00 :
        kineticLbl.configure(text = '주행 상태 : 좌조향')
    elif commands[0] == 0xf3 and commands[2] == 0xb4 :
        kineticLbl.configure(text = '주행 상태 : 우조향')
    elif commands[0] == 0xf1 and commands[2] == 0x64 :
        kineticLbl.configure(text = '주행 상태 : 직진')
    elif commands[0] == 0xf1 and commands[2] == 0x00 :
        kineticLbl.configure(text = '주행 상태 : 좌회전')
    elif commands[0] == 0xf1 and commands[2] == 0xb4 :
        kineticLbl.configure(text = '주행 상태 : 우회전')
    elif commands[0] == 0xf2 and commands[2] == 0x64 :
        kineticLbl.configure(text = '주행 상태 : 후진')
    elif commands[0] == 0xf2 and commands[2] == 0x00 :
        kineticLbl.configure(text = '주행 상태 : 좌조향후진')
    elif commands[0] == 0xf2 and commands[2] == 0xb4 :
        kineticLbl.configure(text = '주행 상태 : 우조향후진')
    main.update()

async def emergencyCHK() :
    global mode
    while True :
        distance = await client.read_gatt_char(uuid2)
        distance = distance.decode().replace('\x00', '')
        disLbl.configure(text = '전방 감지 : %dcm' %int(distance))
        if int(distance) <= 10 :
            disLbl.configure(text = '전방 감지 : 비상 제동')
            messagebox.showerror('경고', '비상 제동')
            mode = 'zero'
            modeState()
            break
        elif mode == 'zero' :
            mode = 'zero'
            modeState()
            break

def spdup() :
    global speed
    speed += 1
    spdLbl.configure(text = 'PositionSpeed : %d' %(speed))
    main.update()

def spddn() :
    global speed
    speed -= 1
    spdLbl.configure(text = 'PositionSpeed : %d' %(speed))
    main.update()

def dpup() :
    global delta_phase
    delta_phase += 0.1
    dpLbl.configure(text = 'Delta Phase : %0.1f' %(delta_phase))
    main.update()

def dpdn() :
    global delta_phase
    delta_phase -= 0.1
    dpLbl.configure(text = 'Delta Phase : %0.1f' %(delta_phase))
    main.update()

def modeInit() :
    global mode
    mode = 'zero'

def camera() :
    os.startfile('"C:/controller/cameraToolsV1.5/exe/cameraTools.exe"')

def carposCHK() :
    global car_x_pos, car_y_pos
    if car_x_pos < 300 and car_y_pos < 400 :
        carposLbl.configure(text = '현재 차량 위치 : 2사분면')
    elif car_x_pos > 300 and car_y_pos < 400 :
        carposLbl.configure(text = '현재 차량 위치 : 1사분면')
    elif car_x_pos < 300 and car_y_pos > 400 :
        carposLbl.configure(text = '현재 차량 위치 : 3사분면')
    elif car_x_pos > 300 and car_y_pos > 400 :
        carposLbl.configure(text = '현재 차량 위치 : 4사분면')
    main.update()

appbg = tk.Label(main, image = appBG).place(x = 0, y = -50)
kineticLbl = tk.Label(main, text = '주행 상태 : 정지', font = 'default 20', fg = 'white', bg = '#3f51b5')
modeLbl = tk.Label(main, text = '현재 모드 : 공회전', font = 'default 20', fg = 'white', bg = '#3f51b5')
stateLbl = tk.Label(main, text = '연결 상태 : Disconnected', font = 'default 20', fg = 'white', bg = '#3f51b5')
posbtn = tk.Button(main, text = 'Positioning On', font = 'default 15', command = positioningSystem, width = 12, height = 2)
connbtn = tk.Button(main, text = '차량 연결', font = 'default 25', command = connEx, width = 10, height = 2)
dirbtn = tk.Button(main, text = '직접 제어', font = 'default 25', command = dirEx, width = 10, height = 3).place(x = 70, y = 300)
autbtn = tk.Button(main, text = '경로주행모드', font = 'default 25', command = auEx, width = 10, height = 3).place(x = 70, y = 450)
writeLinebtn = tk.Button(main, text = '경로 입력', font = 'default 25', command = writeEx, width = 10, height = 3).place(x = 70, y = 600)
posInitbtn = tk.Button(main, text = 'Position initializing', font = 'default 13', command = positionInit, width = 14, height = 1).place(x = 302, y = 110)
carImg = tk.Label(main, image = carimg, bg = '#3f51b5')
backbtn = tk.Button(main, text = '강제 후진', font = 'default 25', command = backEx, width = 10, height = 2).place(x = 70, y = 200)
disLbl = tk.Label(main, text = '전방 감지 : OFF', font = 'default 20', fg = 'white', bg = '#3f51b5')
modeInitbtn = tk.Button(main, text = '모드 초기화', font = 'default 15', command = modeInit, width = 12, height = 2).place(x = 300, y = 669)
camerabtn = tk.Button(main, text = 'Camera Streaming', font = 'default 10', command = camera, width = 15, height = 2).place(x = 850, y = 25)
carposLbl = tk.Label(main, text = '현재 차량 위치 : OFF', font = 'default 20', fg = 'white', bg = '#3f51b5')
stdvectorLbl = tk.Label(main, text = '↑', font = 'default 50', fg = 'white', bg = '#3f51b5').place(x = 839, y = 425)

spdLbl = tk.Label(main, text = 'PositionSpeed : %d' %(speed), font = 'default 12', fg = 'white', bg = '#3f51b5')
spdupbtn = tk.Button(main, text = '▲', command = spdup).place(x = 600, y = 50)
spddnbtn = tk.Button(main, text = '▼', command = spddn).place(x = 600, y = 80)

dpLbl = tk.Label(main, text = 'Delta Phase : %0.1f' %(delta_phase), font = 'default 12', fg = 'white', bg = '#3f51b5')
dpupbtn = tk.Button(main, text = '▲', command = dpup).place(x = 600, y = 110)
dpdnbtn = tk.Button(main, text = '▼', command = dpdn).place(x = 600, y = 140)

spdLbl.place(x = 455, y = 66)
dpLbl.place(x = 455, y = 126)

carposLbl.place(x = 650, y = 270)
modeLbl.place(x = 650, y = 120)
stateLbl.place(x = 650, y = 70)
kineticLbl.place(x = 650, y = 170)
disLbl.place(x = 650, y = 220)
connbtn.place(x = 70, y = 50)
posbtn.place(x = 300, y = 50)
carImg.place(x = 670, y = 400)

main.mainloop()