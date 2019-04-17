import numpy as np
import cv2
import math


class Filters:
    image = None
    filter = None
    cutoff = None
    order = None
    width = None

    def __init__(self, image, filter, cutoff, order=0, width=0):

        self.image = image
        self.cutoff = cutoff
        self.order = order
        self.width = width

        print("**FILTERING**")
        print("Filter = ", filter)
        print("Cutoff = ", cutoff)
        print("Order = ", order)
        print("Width = ", width)

        if filter == 'Ideal High Pass':
            self.filter = self.ideal_high_pass
        elif filter == 'Ideal Low Pass':
            self.filter = self.ideal_low_pass
        elif filter == 'Ideal Band Reject':
            self.filter = self.ideal_BR
        elif filter == 'Ideal Band Pass':
            self.filter = self.ideal_BP
        elif filter == 'Gaussian High Pass':
            self.filter = self.gaussian_high_pass
        elif filter == 'Gaussian Low Pass':
            self.filter = self.gaussian_low_pass
        elif filter == 'Gaussian Band Reject':
            self.filter = self.gaussian_BR
        elif filter == 'Gaussian Band Pass':
            self.filter = self.gaussian_BP
        elif filter == 'Butterworth Band Reject':
            self.filter = self.btw_BR
        elif filter == 'Butterworth Band Pass':
            self.filter = self.btw_BP
        elif filter == 'Butterworth High Pass':
            self.filter = self.butterworth_high_pass
        elif filter == 'Butterworth Low Pass':
            self.filter = self.butterworth_low_pass
        elif filter == 'Laplacian':
            self.filter = self.laplacian


    def find_freq_domain(self, shape):

        N, M = shape
        P = N / 2
        Q = M / 2
        D = np.empty(shape)
        for row in range(D.shape[0]):
            for col in range(D.shape[1]):
                D[row, col] = np.sqrt(((row - P) * (row - P)) + ((col - Q) * (col - Q)))

        return D
    def ideal_high_pass(self, shape, cutoff):

        D = Filters.find_freq_domain(self, shape)
        mask = np.empty(shape)

        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                if D[row, col] <= cutoff:
                    mask[row, col] = 0
                if D[row, col] > cutoff:
                    mask[row, col] = 1

        print("Ideal High Pass")
        return mask

    def ideal_low_pass(self, shape, cutoff):
        mask = 1 - Filters.ideal_high_pass(self, shape, cutoff)
        print("Ideal Low Pass")
        return mask

    def ideal_BR(self, shape, cutoff, width):

        D = Filters.find_freq_domain(self, shape)
        mask = np.empty(shape)

        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                if (cutoff - width / 2 <= D[row, col]) and (D[row, col] <= cutoff + width / 2):
                    mask[row, col] = 0
                else:
                    mask[row, col] = 1

        print("Ideal Band Reject")
        return mask
    def ideal_BP(self, shape, cutoff, width):
        mask = 1 - Filters.ideal_BR(self, shape, cutoff, width)

        print("Ideal Band Pass")
        return mask

    def gaussian_high_pass(self, shape, cutoff):
        D = Filters.find_freq_domain(self, shape)
        mask = np.empty(shape)

        sig = 2 * (cutoff ** 2)

        for row in range(D.shape[0]):
            for col in range(D.shape[1]):
                mask[row, col] = 1 - math.exp(-(D[row, col] ** 2) / sig)

        print("Gaussian High Pass")
        return mask

    def gaussian_low_pass(self, shape, cutoff):
        mask = 1 - Filters.gaussian_high_pass(self, shape, cutoff)

        print("Gaussian Low Pass")
        return mask

    def gaussian_BR(self, shape, cutoff, width):

        D = Filters.find_freq_domain(self, shape)
        mask = np.empty(shape)

        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                if D[row, col] != 0:
                    mask[row, col] = 1 - np.exp(-1 * np.square((np.square(D[row, col]) - np.square(cutoff)) / (D[row, col]
                                                * width)))
                else:
                    mask[row, col] = 1 - np.exp(-1 * np.square((np.square(D[row, col]) - np.square(cutoff)) / width))

        print("Gaussian Band Reject")
        return mask

    def gaussian_BP(self, shape, cutoff, width):
        mask = 1 - Filters.gaussian_BR(self, shape, cutoff, width)

        print("Gaussian Band Pass")
        return mask

    def butterworth_high_pass(self, shape, cutoff, order):
        D = Filters.find_freq_domain(self, shape)
        mask = np.empty(shape)

        newOrder = 2 * order

        for row in range(D.shape[0]):
            for col in range(D.shape[1]):
                mask[row, col] = 1 / (1 + (cutoff / D[row, col]) ** newOrder)

        print("Butterworth High Pass")
        return mask

    def butterworth_low_pass(self, shape, cutoff, order):
        mask = 1 - Filters.butterworth_high_pass(self, shape, cutoff, order)

        print("Butterworth Low Pass")
        return mask

    def btw_BR(self, shape, cutoff, order, width):

        D = Filters.find_freq_domain(self, shape)
        mask = np.empty(shape)

        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                if np.square(D[row, col]) - np.square(cutoff) != 0:
                    mask[row, col] = 1 / (1 + np.power(D[row, col] * width / (np.square(D[row, col]) - np.square(cutoff))
                                                      , 2 * order))
                else:
                    mask[row, col] = 1 / (1 + np.power(D[row, col] * width, 2 * order))

        print("Butterworth Band Reject")
        return mask

    def btw_BP(self, shape, cutoff, order, width):
        mask = 1 - Filters.btw_BR(self, shape, cutoff, order,  width)

        print("Butterworth Band Pass")
        return mask

    def laplacian(self, shape):
        D = Filters.find_freq_domain(self, shape)
        mask = np.empty(shape)

        for row in range(D.shape[0]):
            for col in range(D.shape[1]):
                mask[row, col] = -1 * 4 * np.square(np.pi) * np.square(D[row, col])

        mask = 1 - mask

        print("Laplacian")
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
        if self.filter in [self.ideal_high_pass, self.gaussian_high_pass, self.butterworth_high_pass]:
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

        if self.filter in [self.butterworth_high_pass, self.butterworth_low_pass]:
            mask = self.filter(fshift.shape, int(self.cutoff), int(self.order))
        elif self.filter in [self.btw_BP, self.btw_BR]:
            mask = self.filter(fshift.shape, int(self.cutoff), int(self.order), int(self.width))
        elif self.filter in [self.ideal_BR, self.ideal_BP, self.gaussian_BR, self.gaussian_BP]:
            mask = self.filter(fshift.shape, int(self.cutoff), int(self.width))
        elif self.filter in [self.laplacian]:
            mask = self.filter(fshift.shape)
        else:
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