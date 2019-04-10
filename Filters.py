import numpy as np
from numpy import array
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
        print("Filter = ", filter)
        print("Cutoff = ", cutoff)
        print("Order = ", order)

    def DFT(self):
        print("**DFT**")

        img = self.image
        # 1. Compute the fft of the image
        f = np.fft.fft2(img)
        # 2. shift the fft to center the low frequencies
        fshift = np.fft.fftshift(f)
        # Magnitude of DFT
        magnitude_dft = 20 * np.log(np.abs(fshift))

        return magnitude_dft

    """ Computes forward Fourier transform of input image. 2d matrix image.
        Returns dft. Test runtime speed of self built function with built-in
        np fft - fft2 functions. """
    def built_fft(self):
        print("**Test case (own) DFT**")

        height_img = len(self.image)
        width_img = len(self.image[0])
        pie = math.pi * 2.0

        forward_trans = np.zeros((height_img, width_img), self.image.dtype)
        # for i in range(height_img):
        #     for j in range(width_img):
        #         for m in range(height_img):
        #             for n in range(width_img):
        #                 temp = (pie / height_img) * (i * m + j * n)
        #                 temp_two = math.cos(temp) + math.sqrt(-1) * math.sin(temp)
        #                 temp_two *= self.image[i][j]
        #                 forward_trans[i][j] += temp_two

        return forward_trans

    def mask(self):
        print("**MASK**")


