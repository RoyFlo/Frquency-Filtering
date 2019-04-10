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
        print("Shape: ", shape)
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
        print("Shape: ", shape)
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

    def process(self, image):
        img = image.copy()

        ## Find the min and max
        min = 256
        max = 0
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                if image[row, col] > max:
                    max = image[row, col]
                if image[row, col] < min:
                    min = image[row, col]

        ## Full Contrast Stretch
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                img[row, col] = ((image[row, col] - min)/(max-min)) * 255
        print("Full Contrast Stretch Complete")

        ## Take Negative if High Pass Filter
        if self.filter in [self.ideal_high_pass]:
            print("Taking negative of image.")
            for row in range(image.shape[0]):
                for col in range(image.shape[1]):
                    img[row, col] = 255 - img[row, col]

        return img

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
        # 5. compute the inverse shift1
        f_ishift = np.fft.ifftshift(filtered)
        # 6. compute the inverse fourier transform
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)

        # Full contrast stretch or take negative if needed
        post_img = self.process(img_back)

        print("**COMPLETE**")

        return [magnitude_dft, filtered_dft, post_img]
