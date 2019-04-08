import numpy as np
import cv2
import math

class Filters:
    image = None
    filter = None
    cutoff = None
    order = None

    def __init__(self, image, filter, cutoff, order=0):

        self.image = image
        self.filter = filter
        self.cutoff = cutoff
        self.order = order

        print("**FILTERING**")
        print("Image = ", image)
        print("Filter = ", filter)
        print("Cutoff = ", cutoff)
        print("Order = ", order)
