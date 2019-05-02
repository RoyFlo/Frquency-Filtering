from tkinter import *
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from skimage.io import imread
from decimal import Decimal
import cv2
import time

from Filters import Filters

def is_number(value):
    try:
        value = Decimal(value)
        return True
    except:
        return False


def showimg(img):
    cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    img = np.array(img,dtype=float)/float(255)
    cv2.imshow('test', img)
    cv2.resizeWindow('test', 600, 600)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Creates and sets the size of the GUI window
window = Tk()
window.geometry("1200x900")
window.title("Filtering in Frequency Domain")

# Creates the text for the buttons/entries
Label(window, text="1. Select an Image", font=("Ariel", 12), fg="blue").grid(row=0)
Label(window, text="2. Select Filter", font=("Ariel", 12), fg="blue").grid(row=0, column=1)
Label(window, text="3. Enter Cutoff", font=("Ariel", 12), fg="blue").grid(row=0, column=2)
Label(window, text="4. Enter Order", font=("Ariel", 12), fg="blue").grid(row=0, column=3)
Label(window, text="5. Enter Weight", font=("Ariel", 12), fg="blue").grid(row=0, column=4)
Label(window, text="6. Enter Width", font=("Ariel", 12), fg="blue").grid(row=0, column=5)
Label(window, text="7. Enter X:", font=("Ariel", 12), fg="blue").grid(row=0, column=6)
Label(window, text="   Enter Y:", font=("Ariel", 12), fg="blue").grid(row=0, column=7)


# Sets the defaults of the program
img = "Image2.png"
filter = "Ideal High Pass"
print("Default image is: " + img)
print("Default filter is: " + filter)
cutoff = 15
order = 2


# Changes the image
def iValue(value):
    global img
    #img = value+".png"
    img = value
    print("You have selected " + img)


# Changes the filter
def fValue(value):
    global filter
    filter = value
    print(filter)


iList = ["Image1", "Image2", "Image3", "Image4", "Image5", "Image6"]

filterList = ["Ideal High Pass", "Ideal Low Pass", "Ideal Band Reject", "Ideal Band Pass", "Ideal Notch Reject",
              "Ideal Notch Pass", "Gaussian High Pass", "Gaussian Low Pass", "Gaussian Band Reject",
              "Gaussian Band Pass", "Gaussian Notch Reject", "Gaussian Notch Pass", "Butterworth High Pass",
              "Butterworth Low Pass", "Butterworth Band Reject", "Butterworth Band Pass", "Butterworth Notch Reject",
              "Butterworth Notch Pass" , "Laplacian", ]

# Image Var
var1 = StringVar()
var1.set("Image1")
# Filter Var
var2 = StringVar()
var2.set("Ideal High Pass")
# Cutoff Var
var3 = StringVar()
var3.set(75)
# Order Var
var4 = StringVar()
var4.set(2)
# Weight Var
var5 = StringVar()
var5.set(None)
# Width Var
var6 = StringVar()
var6.set(None)
# Center X - Var
var7 = StringVar()
var7.set(None)
# Center Y - Var
var8 = StringVar()
var8.set(None)

def selectImg():
    imgname = askopenfilename()
    iValue(imgname)


# Image Menu
# setImg = OptionMenu(window, var1, *iList, command=iValue)
setImg = Button(window, text="*Img Select*", command=selectImg, cursor='hand2')
setImg.configure(font="Times")
setImg.grid(row=1, column=0)
# Filter Menu
setFilter = OptionMenu(window, var2, *filterList, command=fValue)
setFilter.configure(font="Times")
setFilter.grid(row=1, column=1)
# Cutoff Entry
setCutoff = Scale(window, from_=15, to=200, orient=HORIZONTAL, cursor='hand2')
setCutoff.configure(font="Times")
setCutoff.grid(row=1, column=2, padx=5)
# Order Entry
setOrder = Scale(window, from_=1, to=20, orient=HORIZONTAL, cursor='hand2')
setOrder.configure(font="Times")
setOrder.grid(row=1, column=3, padx=5)
# Weight Entry
setWeight = Entry(window, textvariable=var5, width=10)
setWeight.configure(font="Times")
setWeight.grid(row=1, column=4, padx=5)
# Width Entry
setWidth = Entry(window, textvariable=var6, width=10)
setWidth.configure(font="Times")
setWidth.grid(row=1, column=5, padx=5)

# Width Entry
setX = Entry(window, textvariable=var7, width=10)
setX.configure(font="Times")
setX.grid(row=1, column=6, padx=5)

# Width Entry
setY = Entry(window, textvariable=var8, width=10)
setY.configure(font="Times")
setY.grid(row=1, column=7, padx=5)

# Figure for the graphs
fig = plt.figure(figsize=(7, 7))
canvas = FigureCanvasTkAgg(fig, master=window)

def run():
    print("***RUNNING***")

    cutoff = setCutoff.get()
    order = setOrder.get()
    width = setWidth.get()
    x_val = setX.get()
    y_val = setY.get()

    # Load image
    print("Uploading " + img)
    image = cv2.imread(img, 0)

    # Timer Start
    start = time.time()
    print("Starting Timer")

    # Filter Image
    obj = Filters(image, filter, cutoff, order, width, x_val, y_val)
    out = obj.FFT()

    # Timer End
    end = time.time()
    print("Timer Stopped")
    t = float("{0:.3f}".format(end-start))
    print("Total Time = ", t)

    # clear old plots
    plt.clf()

    # Image display
    a1 = fig.add_subplot(221)
    a1.imshow(image, cmap='binary_r')
    a1.axis('off')
    a1.set_title("Original Image")

    # DFT graph
    a2 = fig.add_subplot(222)
    a2.imshow(out[0], cmap='binary_r')
    a2.xaxis.set_visible(False)
    a2.yaxis.set_visible(False)
    a2.set_title("Magnitude DFT")

    # Mask graph
    a3 = fig.add_subplot(223)
    a3.imshow(out[1], cmap='binary_r')
    a3.set_facecolor('k')
    a3.xaxis.set_visible(False)
    a3.yaxis.set_visible(False)
    a3.set_title("Mask")

    # Resulting Image display

    """if there is a value inside of the Weight field,
    the program assumes to use unsharp, otherwise
    it uses original filter"""
    if is_number(setWeight.get()):
        # output_dir = 'output/'
        # output_image_name = output_dir + "_" + datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
        outName = "output/result.png"
        image1 = np.int32(image)
        image2 = np.int32(out[2])
        diff = image1 - image2
        unsharpImage = (image + (float(setWeight.get()) * diff))
        cv2.imwrite(outName, unsharpImage)
        # writes the image first, then displays the result. Doing this the other way around causes imshow to display a different image
        resultImage = cv2.imread('output/result.png', 0)
        a4 = fig.add_subplot(224)
        a4.imshow(resultImage, cmap='binary_r')
        a4.set_title("Filtered Image")

    else:
        a4 = fig.add_subplot(224)
        a4.imshow(out[2], cmap='binary_r')
        a4.axis('off')
        a4.set_title("Filtered Image")

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().grid(row=2, columnspan=6)

    # print time
    t1 = str(t)
    msg = "Time Elapsed: " + t1
    Label(window, text=msg, font=("Times", 15), fg="red").grid(row=3, sticky=NE)
    canvas.draw()


# RUN button
button1 = Button(window, text="**RUN**", bg="red", font=("Times", 15), command=run, cursor='spraycan')
button1.grid(row=1, column=8, padx=30, pady=15)

window.mainloop()