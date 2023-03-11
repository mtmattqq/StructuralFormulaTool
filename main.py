import pygame
import tkinter

window = tkinter.Tk()
window.title("視窗元件配置")
window.geometry("300x28")

def varify():
    a=0

varifyCode=tkinter.Entry(width=20, font=("Arial", 14, "bold"), bg="light gray", fg="black", state=tkinter.NORMAL)
varifyCode.insert(tkinter.END, string="some text")
varifyCode.place(x=0,y=0)
varifyCode.get()

varifyButton=tkinter.Button(text="confirm", font=("Arial", 14, "bold"), padx=5, pady=5, bg="gray", fg="black", command=varify)

window.mainloop()

# pygame.init()