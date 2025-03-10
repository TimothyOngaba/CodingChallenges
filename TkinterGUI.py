from tkinter import *
from PIL import Image, ImageTk  # Requires `pip install pillow`


root = Tk()
root.title("Calculator")

root.geometry("400x600")
icon = ImageTk.PhotoImage(file="/home/tim/Pictures/cyclist.png")  # Use a PNG instead
root.tk.call('wm', 'iconphoto', root._w, icon)  

my_lable = Label(root, text="Wagwan Braddah!", fg="blue", bg="red",  font=("Helvetica", 32))
my_lable.pack()

my_lable2 = Label(root, text="Fist bump", fg="black", bg="white",  font=("arial", 32))
my_lable2.pack(pady=15)








root.mainloop()
