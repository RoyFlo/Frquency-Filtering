from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from skimage.io import imread
import skimage.transform as skt

#Creates and sets the size of the GUI window
window = Tk()
window.geometry("700x820")
window.title("Filtering in Frequency Domain")

# Creates the instructions for the buttons
Label(window, text="1. Select an Image", font=("Ariel", 12), fg="blue").grid(row=0)
Label(window, text="2. Select Filter", font=("Ariel", 12), fg="blue").grid(row=0, column=1)
Label(window, text="3. Enter Cutoff", font=("Ariel", 12), fg="blue").grid(row=0, column=2)
Label(window, text="4. Enter Order", font=("Ariel", 12), fg="blue").grid(row=0, column=3)
# Label(window, text="5. RUN", font=("Ariel", 12), fg="blue").grid(row=0, column=5)



# Sets the defualts of the program
img = "Image1.png"
filter = "Filter 1"
print("Default image is " + img + " and will filter using " + filter)

# Changes the test phantoms to be simulated
def iValue(value):
    global img
    img = value+".png"
    print("You have selected " + img)

# Changes the scale factor to get the new output image resolution to be simulated
def fValue(value):
    global filter
    filter = value
    print(filter)

def run():

    cutoff = setCutoff.get()
    order = setOrder.get()
    print("Image = ", img)
    print("Filter = ", filter)
    print("Cutoff = ", cutoff)
    print("Order = ", order)


iList = ["Image1", "Image2", "Image3", "Image4", "Image5", "Image6"]
sList = [1,2,3,4,5,6,7,8,9,10]
filterList = ["Filter 1", "Filter 2"]

# Image
var1 = StringVar()
var1.set("Image1")

# Filter
var2 = StringVar()
var2.set("Filter 1")

# Cutoff
var3 = StringVar()
var3.set(15)

# Order
var4 = StringVar()
var4.set(2)

set1 = OptionMenu(window, var1, *iList, command=iValue)
set1.configure(font=("Ariel"))
set1.grid(row=1, column=0)

set2 = OptionMenu(window, var2, *filterList, command=fValue)
set2.configure(font=("Ariel"))
set2.grid(row=1, column=1)

setCutoff = Entry(window, textvariable=var3)
setCutoff.grid(row=1, column=2)

setOrder = Entry(window, textvariable=var4)
setOrder.grid(row=1, column=3)


#print(img, filter, order, cutoff)

fig = Figure(figsize=(7, 7))

button1 = Button(window, text="**RUN**", bg="red", command=run)
button1.grid(row=1, column=5)

window.mainloop()