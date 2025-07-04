import tkinter as tk  # MADE BY XTRON (MUHAMMED AKYUZ) --> SCRIPT DEV
import datetime
from tkinter import messagebox
import time
import random
import platform
from PIL import Image, ImageTk
import cv2
import sys
import os

def resource_path(relative_path):
    """PyInstaller için dosya yolu çözümü"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


linux = "Linux"
windows = "Windows"
macos = "MacOS"

plats = platform.system()


def print_clock():
    time_current = datetime.datetime.now().strftime("%H:%M:%S")
    label_time.config(text=time_current)
    root.after(1000, print_clock)


def slow_print_label_welcome(text_v, index=0):
    if index < len(text_v):
        label_welcome.config(text=label_welcome.cget("text") + text_v[index])
        root.after(200, slow_print_label_welcome, text_v, index + 1)


def slow_print_label_ask(text_v, index=0):
    if index < len(text_v):
        label_ask.config(text=label_ask.cget("text") + text_v[index])
        root.after(200, slow_print_label_ask, text_v, index + 1)
    else:
        button_yes.place(x=300, y=300)
        button_no.place(x=600, y=300)


def button_no_command():
    messagebox.showerror("BYE BYE...", "COUNT 3 SECONDS :)")
    time.sleep(3)
    if plats == windows:
        os.system("shutdown /s /t 0")
    elif plats == macos or linux:
        os.system("sudo shutdown now")


def button_yes_command():
    root.destroy()
    gameroot = tk.Tk()
    gameroot.geometry("1000x600")
    cap = cv2.VideoCapture(resource_path("animationeffectpython.mp4"))
    panel = tk.Label(gameroot)
    panel.place(x=0, y=0)

    score = 0

    def slow_print_label_alright(text_v, index=0):
        if index < len(text_v):
            label_alright.config(text=label_alright.cget("text") + text_v[index])
            gameroot.after(200, slow_print_label_alright, text_v, index + 1)
        else:
            label_alright.destroy()
            start_game()

    def start_game():
        canvas = tk.Canvas(gameroot, width=1000, height=600, bg="white")
        canvas.pack()
        label_score = tk.Label(gameroot, text=f"Score: {score}", font=("Impact", 20))
        label_score.place(x=10, y=10)

        label_catch100balls_until1_minute = tk.Label(gameroot,text="CATCH THESE  100 BALLS UNTIL 1 MINUTE OR YOU SUFFER THE CONSEQUENCES")
        label_catch100balls_until1_minute.place(x=250,y=300)


        def start_stopwatch():
            counter = 60 
            def update_timer():
                nonlocal counter
                if counter >= 0:
                    label_stopwatch.config(text=f"Time: {counter}")
                    counter -= 1
                    gameroot.after(1000, update_timer)
                else:
                    if score >= 100:
                        messagebox.showinfo("Time's up!", "Well you're good")
                        gameroot.destroy()
                        
                    else:
                        messagebox.showinfo("Time's up!", "Time finished! And say good bye to your computer")
                        gameroot.destroy()
                        if plats == windows:
                            os.system("shutdown /s /t 0")
                        elif plats == macos or linux:
                            os.system("sudo shutdown now")




            label_stopwatch = tk.Label(gameroot, text="", font=("Impact", 20))
            label_stopwatch.place(x=450, y=10)
            update_timer()


        start_stopwatch()
        time.sleep(2)
        label_catch100balls_until1_minute.destroy()

        def create_circle():
            x = random.randint(50, 950)
            y = random.randint(50, 550)
            r = 30
            circle = canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="black")
            canvas.tag_bind(circle, "<Button-1>", lambda event: increase_score(circle))

        def increase_score(circle_id):
            nonlocal score
            score += 1
            label_score.config(text=f"Score: {score}")
            canvas.delete(circle_id)
            create_circle()

        create_circle()

    label_alright = tk.Label(gameroot, text="", font=("Impact", 24))
    

    def play_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (1000, 600))
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            panel.config(image=img)
            panel.image = img
            gameroot.after(30, play_video)
        else:
            cap.release()
            panel.destroy()
            label_alright.pack(padx=150, pady=150)
            slow_print_label_alright("ALRIGHT, THEN LET'S GET STARTED ")

    play_video()
    gameroot.mainloop()


root = tk.Tk()
root.title("Game")
root.geometry("1000x600")
root.resizable(width=False, height=False)

label_welcome = tk.Label(root, text="", font=("Impact", 24))
label_welcome.place(x=20, y=10)

label_ask = tk.Label(root, text="", font=("Impact", 24))
label_ask.place(x=350, y=40)

label_time = tk.Label(root, text="", font=("Impact", 24))
label_time.pack(anchor="n")

button_yes = tk.Button(root, text="YES !", font=("Impact", 24), width=5, command=button_yes_command)
button_no = tk.Button(root, text="NO !", font=("Impact", 24), width=5, command=button_no_command)

print_clock()
slow_print_label_welcome("WELCOME PLAYER")
slow_print_label_ask("DO U WANNA PLAY GAME?")

root.mainloop()
