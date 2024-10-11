from ModuleIntegrated import *

main = Tk()
main.title('차랑재어')
main.geometry('1024x768')
main.resizable(width = FALSE, height = FALSE)

def mf1() :
    isconLbl.configure(text = 1)
def mf2() :
    isconLbl.configure(text = 2)
def mf3() :
    isconLbl.configure(text = 3)

isconLbl = Label(main, text = '연결 상테 : Disconnected', font = 'default 20')
dirbtn = Button(main, text = '차량 연결', font = 'default 25', command = mf1, width = 10, height = 3).place(x = 70, y = 50)
dirbtn = Button(main, text = '직접재어', font = 'default 25', command = mf1, width = 10, height = 3).place(x = 70, y = 300)
autbtn = Button(main, text = '경로주행모드', font = 'default 25', command = mf2, width = 10, height = 3).place(x = 70, y = 450)
writeLinebtn = Button(main, text = '경로 읽기', font = 'default 25', command = mf3, width = 10, height = 3).place(x = 70, y = 600)
isconLbl.place(x = 600, y = 70)

main.mainloop()
