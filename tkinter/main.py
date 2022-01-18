import threading
import tkinter
import twitter
import tkinter.ttk
from tkinter import *
import pyupbit
from functools import partial

window = tkinter.Tk()

access_key = "I17qwDwCd4xgU1cOD6upkppDV0b0c1wCLvetw760"
secret_key = "T9x0ae8j5B6sO98NY1Vvmzc5aaAkJgQlRp8yr1B9"

t_consumer_key = "agLXI1dXGBKA5dMEGt7qIMu1P"
t_consumer_secret = "GNU7YH9rEOF3PTzGyPRg3wgtH2Bu9pD0qlccdcoqWWMK3nNr6O"

t_access_token = "1473502327575576584-mirZ1Nuyd078ro1MdvgzVYOyPGpjyT"
t_access_token_secret = "H0iS1S1Epaou6prCalJ4IvzIECtv1gZtri0mHMN7Z7Cib"

twitter_api = twitter.Api(consumer_key=t_consumer_key,
                          consumer_secret=t_consumer_secret,
                          access_token_key=t_access_token,
                          access_token_secret=t_access_token_secret)

window.title("인턴 프로젝트")
window.geometry("680x640")  #너비X높이+X좌표+Y좌표
window.resizable(True, True)        #사이즈 변경 가능
Label1 = Label(window, text="찾고자하는 사람의 트위터 아이디를 입력하세요 : ")
Label1.place(x = 10, y = 50)
box=tkinter.Entry(window)
box.place(x = 300, y = 50,width=200, height=30)
box.configure(font=(15))
Label2 = Label(window, text="찾고자하는 단어를 입력하세요 : ")
Label2.place(x = 10, y = 100)
box2=tkinter.Entry(window)
box2.place(x = 300, y = 100,width=200, height=30)
box2.configure(font=(15))
box4 = tkinter.Entry(window)
box4.place(x=70, y=150)
box5 = tkinter.Entry(window)
box5.place(x=280, y=150, width=100)
box6 = tkinter.Entry(window)
box6.place(x=440, y=150, width=50)
Label9 = Label(window, text="코인명 : ")
Label9.place(x=10, y=150)
Label10 = Label(window, text="가격 : ")
Label10.place(x=240, y=150)
Label11 = Label(window, text="갯수 : ")
Label11.place(x=400, y=150)
Label5 = Label(window, text="찾으시는 코인의 이름을 입력해주세요 : ")
Label5.place(x = 10, y = 200)
Label5.config(font=8)
box3=tkinter.Entry(window)
box3.place(x = 380, y = 200, width=200, height=30)
Label8 = Label(window, text="설정을 선택해주세요 : ")
Label8.place(x = 10, y = 250)
Label8.config(font=8)
a = ["Month", "Day", "Hour", "Minute"]
combobox = tkinter.ttk.Combobox(window)
combobox.config(values=a)
combobox.config(state="readonly")
combobox.set("단위설정")
combobox.place(x = 230, y = 250, height=30)
b = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
combobox2 = tkinter.ttk.Combobox(window)
combobox2.config(values=b)
combobox2.config(state="readonly")
combobox2.set("갯수설정")
combobox2.place(x = 400, y = 250, height=30)
Label7 = Label(window)

def th():
    th = threading.Thread(target=Streaming)
    th.daemon = True
    th.start()
    if button2['text'] == "Streaming":
        button2['text'] = "Streaming\n중"
    else:
        button2['text'] = "Streaming"
        th.raise_exception()

def Streaming():
    name = box.get()
    word = box2.get()
    stream = twitter_api.GetStreamFilter(track=[word])
    for tweets in stream:
        tweet = tweets["user"]['screen_name']
        if tweet == name:
            if box4.get() and box5.get() and box6.get():
                Buy()
            window2 = tkinter.Tk()
            window2.title("새로운 알림이 있습니다")
            window2.geometry("500x200")
            Label3 = Label(window2, text=tweets["text"])
            Label3.place(x = 50, y = 50)
            Label3.config(font=15)
            Label4 = Label(window2, text=tweets["created_at"])
            Label4.place(x = 50, y = 80)
            window2.mainloop()

def Timeline():
    window3 = tkinter.Tk()
    window3.title("타임라인 전체 보기")
    window3.geometry("700x400")
    name = box.get()
    word = box2.get()
    tweet = twitter_api.GetUserTimeline(screen_name=name, count=50, include_rts=True, exclude_replies=False)
    result = []
    j = 0
    for i in tweet:
        result.append([i.text, i.created_at])

    for p in result:
        if any(word in s for s in p):
            Label6 = Label(window3, text=p)
            Label6.place(x = 20, y = 40+j*30)
            j += 1
    window3.mainloop()

def Search():
    Label7.config(text="")
    coin = box3.get()
    filter = combobox.get().lower()
    count2 = combobox2.get()
    if filter == "hour":
        filter = "minute60"
    elif filter == "minute":
        filter = " minute1"
    price = pyupbit.get_ohlcv(coin, interval=filter, count=int(count2))
    Label7.config(text=price, justify="left")
    Label7.place(x=10, y=300)

def Buy():
    upbit = pyupbit.Upbit(access_key, secret_key)
    Buy1 = upbit.buy_limit_order(box4.get(), int(box5.get()), int(box6.get()))
    if Buy1 != None:
        f = open("Buy.txt", 'a')
        f.write(box4.get())
        f.write(' ')
        f.write(box5.get())
        f.write(' ')
        f.write(box6.get())
        f.write(' ')
        f.write(Buy1['uuid'])
        f.write('\n')
        f.close()
        box4.delete(0, "end")
        box5.delete(0, "end")
        box6.delete(0, "end")
        window4 = tkinter.Tk()
        window4.title("주문 완료")
        window4.geometry("300x100")
        Label13 = Label(window4, text="매수 주문 완료")
        Label13.place(x=40, y=40)
        Label13.config(font=15)
        window4.mainloop()

def Sell():
    upbit2 = pyupbit.Upbit(access_key, secret_key)
    upbit2.sell_limit_order(box4.get(), int(box5.get()), int(box6.get()))
    f = open("Sell.txt", 'a')
    f.write(box4.get())
    f.write(' ')
    f.write(box5.get())
    f.write(' ')
    f.write(box6.get())
    f.write('\n')
    f.close()
    box4.delete(0, "end")
    box5.delete(0, "end")
    box6.delete(0, "end")

def Check():
    window4 = tkinter.Tk()
    window4.title("주문내역 전체 보기")
    window4.geometry("700x450")
    Label13 = Label(window4, text="구매 예약 내역")
    Label13.place(x = 30, y =10)
    Label13.config(font=15)
    Label14 = Label(window4, text="판매 예약 내역")
    Label14.place(x=30, y=200)
    Label14.config(font=15)
    m = 0
    n = 0
    f = open("Sell.txt", "r")
    while True:
        st1 = f.readline().split()
        if st1 == []:
            break
        Label12 = Label(window4, text="코인 " + st1[0] + "를 " + st1[1] + "원에 " + st1[2] + "개 만큼 매도 주문하였습니다.")
        Label12.place(x=30 + 350 * m, y=230 + 20 * n)
        button7 = tkinter.Button(window4, text="x", overrelief="solid", width=20)
        button7.config(command=partial(delete, st1[0], window4, 0, st1[3]))
        button7.place(x=10 + 350 * m, y=230 + 20 * n, width=20, height=20)
        n += 1
        if n == 7:
            m = 1
            n = 0
    n = 0
    m = 0
    f = open("Buy.txt", "r")
    while True:
        st = f.readline().split()
        if st == []:
            break
        Label12 = Label(window4, text= "코인 " + st[0] + "를 " + st[1] + "원에 " + st[2] + "개 만큼 매수 주문하였습니다.")
        Label12.place(x=30 + 350*m , y=40 + 20*n)
        button7 = tkinter.Button(window4, text="x", overrelief="solid", width=20)
        button7.config(command=partial(delete, st[0], window4, 1, st[3]))
        button7.place(x=10 + 350*m, y=40 + 20*n, width=20, height=20)
        n += 1
        if n == 7:
            m = 1
            n = 0

def delete(st,window,a, st1):
    window.destroy()
    window5 = tkinter.Tk()
    window5.title("삭제 완료")
    window5.geometry("250x100")
    Label13 = Label(window5, text="삭제되었습니다.")
    Label13.place(x=30, y=30)
    upbit = pyupbit.Upbit(access_key, secret_key)
    upbit.cancel_order(st1)
    if a == 1:
        with open("Buy.txt","r") as f:
            lines = f.readlines()
        with open("Buy.txt","w") as f:
            for line in lines:
                if st not in line.strip("\n"):
                    f.write(line)
    elif a == 0:
        with open("Sell.txt","r") as f:
            lines = f.readlines()
        with open("Sell.txt","w") as f:
            for line in lines:
                if st not in line.strip("\n"):
                    f.write(line)
    Check()

button = tkinter.Button(window, text="Timeline", overrelief="solid", width=20)
button.config(command=Timeline)
button.place(x = 520, y = 50, width=60, height=80)
button2 = tkinter.Button(window, text="Streaming", overrelief="solid", width=20)
button2.config(command=th)
button2.place(x = 590, y = 50, width=60, height=80)
button4 = tkinter.Button(window, text="Buy", overrelief="solid", width=20)
button4.place(x=505, y=150, width=80, height=20)
button4.config(command=Buy)
button5 = tkinter.Button(window, text="Sell", overrelief="solid", width=20)
button5.place(x=590, y=150, width=80, height=20)
button5.config(command=Sell)
button3 = tkinter.Button(window, text="Search", overrelief="solid", width=20)
button3.place(x=590, y = 250, width=80, height=30)
button3.config(command=Search)
button6 = tkinter.Button(window, text="주문내역 보기", overrelief="solid", width=20)
button6.place(x=10, y = 550, width=120, height=60)
button6.config(command=Check)

window.mainloop()
