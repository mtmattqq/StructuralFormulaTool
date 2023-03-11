import pygame
import tkinter
from tkinter import filedialog

def get_file_path():
    file_path=filedialog.askopenfilename()
    # print the selected file path
    print("Selected file:", file_path)
    return file_path

window=tkinter.Tk()
window.title("產品驗證")
window.geometry("500x40")

def varify():
    varifyCode.get()
    window.quit()

hintText=tkinter.Label(
    text="Enter varify code ",
    font=("Arial", 14, "bold"),
    padx=0, pady=0,
    bg="white", fg="black",
    highlightthickness=0,
)
hintText.grid(row=0, column=0)

varifyCode=tkinter.Entry(
    width=20,
    font=("Arial", 14, "bold"),
    bg="light gray", fg="black",
    state=tkinter.NORMAL
)
varifyCode.grid(row=0, column=1)


varifyButton=tkinter.Button(
    text="confirm",
    font=("Arial", 14, "bold"),
    padx=2, pady=0,
    bg="light gray", fg="black",
    command=varify
)
varifyButton.grid(row=0,column=2)

window.mainloop()





