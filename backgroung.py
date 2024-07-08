import tkinter as tk
from tkinter import PhotoImage
import subprocess

def run_gesture():
    subprocess.run(["python","gesture.py"])

def run_voice():

    subprocess.run(["python","voice.py"])
   
root=tk.Tk()
root.title("Virtual Mouse")
root.geometry("1500x1000")
image_path=PhotoImage(file="D:/vm5.png")
bg_image=tk.Label(root,image=image_path)
bg_image.place(relheight=1, relwidth=1)

color1 = '#1589FF'
color2 = 'BLACK'

'''main_frame = tk.Frame(root, bg=color1, pady=40)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)'''


button1 = tk.Button(
    bg_image,
    background=color1,
    foreground=color2,
    highlightthickness=2,
    highlightbackground=color2,
    highlightcolor='WHITE',
    width=10,
    height=2,
    border=0,
   #cursor='hand1',
    text='GESTURE',
    font=('Arial',16,'bold'),
    command=run_gesture
)
#button1.grid(column=0, row=0, pady=5)
button1.place(x=575, y=275)

button2 = tk.Button(
    bg_image,
    background=color1,
    foreground=color2,
    activebackground=color2,
    highlightthickness=2,
    highlightbackground=color2,
    highlightcolor='WHITE',
    width=10,
    height=2,
    border=0,
    #cursor='hand1',
    text='VOICE',
    font=('Arial',16,'bold'),
    command=run_voice
)
#button2.grid(column=0, row=1, pady=5)
button2.place(x=575, y=350)

'''text_label=tkinter.Label(root, text='Welcome to My App', font=('Georgia',24))
text_label.pack()'''

root.mainloop()
