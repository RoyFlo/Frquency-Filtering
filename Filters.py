import numpy as np
from numpy import array
import cv2
import math
import cmath




class Filters:
    image = None
    filter = None
    cutoff = None
    order = None
    width = None
    weight = None
    x_val = None
    y_val = None
    whichFFT = 0

    def __init__(self, image, filter, cutoff, order=0, width=0, weight=0, x_val=0, y_val=0, whichFFT=0):


        self.image = image
        self.cutoff = cutoff
        self.order = order
        self.width = width
        self.weight = weight
        self.x_val = x_val
        self.y_val = y_val
        self.whichFFT = whichFFT


        print("**FILTERING**")
        print("Filter = ", filter)
        print("Cutoff = ", cutoff)
        print("Order = ", order)
        print("Width = ", width)
        print("Weight = ", weight)
        print("Center = (",x_val, ", ", y_val,")")
        if whichFFT == 0:
            print("Built-in FFT")
        if whichFFT == 1:
            print("Own FFT")


        if filter == 'Ideal High Pass':
            self.filter = self.ideal_high_pass
        elif filter == 'Ideal Low Pass':
            self.filter = self.ideal_low_pass
        elif filter == 'Ideal Band Reject':
            self.filter = self.ideal_BR
        elif filter == 'Ideal Band Pass':
            self.filter = self.ideal_BP
        elif filter == 'Ideal Notch Reject':
            self.filter = self.ideal_NR
        elif filter == 'Ideal Notch Pass':
            self.filter = self.ideal_NP
        elif filter == 'Gaussian High Pass':
            self.filter = self.gaussian_high_pass
        elif filter == 'Gaussian Low Pass':
            self.filter = self.gaussian_low_pass
        elif filter == 'Gaussian Band Reject':
            self.filter = self.gaussian_BR
        elif filter == 'Gaussian Band Pass':
            self.filter = self.gaussian_BP
        elif filter == 'Gaussian Notch Reject':
            self.filter = self.gaussian_NR
        elif filter == 'Gaussian Notch Pass':
            self.filter = self. gaussian_NP
        elif filter == 'Butterworth Band Reject':
            self.filter = self.btw_BR
        elif filter == 'Butterworth Band Pass':
            self.filter = self.btw_BP
        elif filter == 'Butterworth High Pass':
            self.filter = self.butterworth_high_pass
        elif filter == 'Butterworth Low Pass':
            self.filter = self.butterworth_low_pass
        elif filter == 'Butterworth Notch Reject':
            self.filter = self.btw_NR
        elif filter == 'Butterworth Notch Pass':
            self.filter = self.btw_NP
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

    def notch_freq_domain(self, shape, x_val, y_val):

        N, M = shape
        P = N / 2
        Q = M / 2
        D = np.empty(shape)
        for row in range(D.shape[0]):
            for col in range(D.shape[1]):
                D[row, col] = np.sqrt(np.square(row - P - x_val) + np.square(col - Q - y_val))

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
        highPass = Filters.ideal_high_pass(self, shape, cutoff)
        mask = 1 - highPass

        if float(self.weight) == 0:
            print("Ideal Low Pass")
            return mask
        else:
            print("Unsharp Ideal Low Pass")

            return 1 + ((float(self.weight))*highPass)

            # return (1-weightVar) * mask + weightVar


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

    def ideal_NR(self, shape, cutoff, x_val, y_val):
        D1 = Filters.notch_freq_domain(self, shape, x_val, y_val)
        D2 = Filters.notch_freq_domain(self, shape, -x_val, -y_val)
        mask = np.empty(shape)
        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                if (D1[row, col] <= cutoff) or (D2[row, col] <= cutoff):
                    mask[row, col] = 0
                else:
                    mask[row, col] = 1

        print("Ideal Notch Reject")

        return mask

    def ideal_NP(self, shape, cutoff, x_val, y_val):
        mask = 1 - Filters.ideal_NR(self, shape, cutoff, x_val, y_val)

        print("Ideal Notch Pass")

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
        highPass = Filters.gaussian_high_pass(self, shape, cutoff)
        mask = 1 - highPass

        if float(self.weight) == 0:

            print("Gaussian Low Pass")
            return mask
        else:
            print("Unsharp Gaussian Low Pass")

            return 1 + ((float(self.weight))*highPass)

            # return (1-weightVar) * mask + weightVar

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

    def gaussian_NR(self, shape, cutoff, x_val, y_val):
        D1 = Filters.notch_freq_domain(self, shape, x_val, y_val)
        D2 = Filters.notch_freq_domain(self, shape, -x_val, -y_val)
        mask = np.empty(shape)

        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                mask[row, col] = 1 - math.exp(-.5 * ((D1[row, col] * D2[row, col])/np.square(cutoff)))

        print("Gaussian Notch Reject")

        return mask

    def gaussian_NP(self, shape, cutoff, x_val, y_val):
        mask = 1 - Filters.gaussian_NR(self, shape, cutoff, x_val, y_val)

        print("Gaussian Notch Pass")
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
        highPass = Filters.butterworth_high_pass(self, shape, cutoff, order)
        mask = 1 - highPass

        if float(self.weight) == 0:

            print("Butterworth Low Pass")
            return mask
        else:
            print("Unsharp Butterworth Low Pass")

            return 1 + ((float(self.weight))*highPass)

            # return (1-weightVar) * mask + weightVar

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

    def btw_NR(self, shape, cutoff, order, x_val, y_val):
        D1 = Filters.notch_freq_domain(self, shape, x_val, y_val)
        D2 = Filters.notch_freq_domain(self, shape, -x_val, -y_val)
        mask = np.empty(shape)

        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                if D1[row, col] * D2[row, col] != 0:
                    mask[row, col] = 1 / (1 + np.power(np.square(cutoff)/(D1[row, col] * D2[row, col]), order))
                else:
                    mask[row, col] = 1 / (1 + np.power(np.square(cutoff), order))

        print("Butterworth Notch Reject")
        return mask

    def btw_NP(self, shape, cutoff, order, x_val, y_val):
        mask = 1 - Filters.btw_NR(self, shape, cutoff, order, x_val, y_val)

        print("Butterworth Notch Pass")
        return mask

    def laplacian(self, shape):
        D = Filters.find_freq_domain(self, shape)
        D = D / np.max(D)
        mask = np.empty(shape)

        for row in range(D.shape[0]):
            for col in range(D.shape[1]):
                mask[row, col] = 1 + 4. * np.square(np.pi) * np.square(D[row, col])

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

        weightVar = float(self.weight)
        if weightVar == 0:
            print("not unsharp")
        else:
            print("unsharp")

        img = self.image
        # 1. Compute the fft of the image
        if(self.whichFFT == 1):
            f = self.fft_symmetry(img)
        if(self.whichFFT == 0):
            f = np.fft.fft2(img)
        # 2. shift the fft to center the low frequencies
        fshift = np.fft.fftshift(f)

        if self.filter in [self.butterworth_high_pass, self.butterworth_low_pass]:
            mask = self.filter(self.image.shape, int(self.cutoff), int(self.order))
        elif self.filter in [self.btw_BP, self.btw_BR]:
            mask = self.filter(fshift.shape, int(self.cutoff), int(self.order), int(self.width))
        elif self. filter in [self.btw_NR, self.btw_NP]:
            mask = self.filter(fshift.shape, int(self.cutoff), int(self.order), int(self.x_val), int(self.y_val))
        elif self.filter in [self.ideal_BR, self.ideal_BP, self.gaussian_BR, self.gaussian_BP]:
            mask = self.filter(fshift.shape, int(self.cutoff), int(self.width))
        elif self.filter in [self.ideal_NR, self.ideal_NP, self.gaussian_NR, self.gaussian_NP]:
            mask = self.filter(fshift.shape, int(self.cutoff), int(self.x_val), int(self.y_val))
        elif self.filter in [self.laplacian]:
            mask = self.filter(self.image.shape)
        else:
            mask = self.filter(self.image.shape, int(self.cutoff))

        
        #filter the image
        filteredImage = fshift * mask
        
        #compute the inverse shift
        inverseShift = np.fft.ifftshift(filteredImage)
        
        #compute the inverse FFT
        inverseFFT = np.fft.ifft2(inverseShift)

        #compute the magnitude
        magnitude = np.absolute(inverseFFT)
        
        magDFT = np.log(np.absolute(fshift))
        magDFT = self.process(magDFT).astype('uint8')

        magFiltered = magDFT * mask
        post = self.process(magnitude).astype('uint8')
        
        print("**COMPLETE**")
        return [magDFT, magFiltered,post]

    def fft_symmetry(self, matrix):
        """Computes the forward Fourier transform using symmetry"""

        (h, w) = matrix.shape
        fwd_trans = np.array([[sum([(matrix[i][j] * cmath.exp(-1 * 1j * ((2*math.pi)/h) * (u*i + v*j)))
                                    for i in range(h) for j in range(w)]) for v in range(w)] for u in range((h//2)+1)])

        fwd_mirror = [i[::-1] for i in fwd_trans[(h//2)-1:0:-1]]
        mirror = array(fwd_mirror)

        a = np.concatenate((fwd_trans, mirror))

        return a

