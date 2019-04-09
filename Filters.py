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
        print("Filter = ", filter)
        print("Cutoff = ", cutoff)
        print("Order = ", order)

        if filter == 'Ideal High Pass':
            self.filter = self.ideal_high_pass
        elif filter == 'Ideal Low Pass':
            self.filter = self.ideal_low_pass

    def ideal_high_pass(self, shape, cutoff):
        N, M = shape
        P = N / 2
        Q = M / 2

        D = np.empty(shape)
        mask = np.empty(shape)

        for row in range(D.shape[0]):
            for col in range(D.shape[1]):
                D[row, col] = np.sqrt(((row - P) * (row - P)) + ((col - Q) * (col - Q)))

        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                if D[row, col] <= cutoff:
                    mask[row, col] = 0
                if D[row, col] > cutoff:
                    mask[row, col] = 1

        print("Ideal High Pass")
        return mask

    def ideal_low_pass(self, shape, cutoff):
        N, M = shape
        P = N/2
        Q = M/2

        D = np.empty(shape)
        mask = np.empty(shape)

        for row in range(D.shape[0]):
            for col in range(D.shape[1]):
                D[row, col] = np.sqrt(((row - P)*(row - P)) + ((col - Q)*(col - Q)))

        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                if D[row, col] <= cutoff:
                    mask[row, col] = 1
                if D[row, col] > cutoff:
                    mask[row, col] = 0

        print("Ideal Low Pass")
        return mask

    def FFT(self):
        print("**FFT**")

        img = self.image
        # 1. Compute the fft of the image
        f = np.fft.fft2(img)
        # 2. shift the fft to center the low frequencies
        fshift = np.fft.fftshift(f)
        # Magnitude of DFT
        magnitude_dft = 20 * np.log(np.abs(fshift))

        mask = self.filter(fshift.shape, int(self.cutoff))

        # Apply mask to shifted DFT
        filtered = fshift * mask

        # Magnitude of filtered DFT
        filtered_dft = 20 * np.log(np.abs(filtered))

        return [magnitude_dft, filtered_dft]
