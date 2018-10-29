import numpy as np
from scipy.misc import imread, imshow
from scipy import ndimage
import matplotlib.pyplot as plt
import imageio 
from PIL import Image 
import cv2 
 
def GetBilinearPixel(imArr, posX, posY):
    out = []
 
    #Get integer and fractional parts of numbers 
    modXi = int(posX) 
    modYi = int(posY) 
    modXf = posX - modXi 
    modYf = posY - modYi 
    modXiPlusOneLim = min(modXi+1,imArr.shape[1]-1)
    modYiPlusOneLim = min(modYi+1,imArr.shape[0]-1)
 
    #Get pixels in four corners
    for chan in range(imArr.shape[2]):
        bl = imArr[modYi, modXi, chan]
        br = imArr[modYi, modXiPlusOneLim, chan]
        tl = imArr[modYiPlusOneLim, modXi, chan]
        tr = imArr[modYiPlusOneLim, modXiPlusOneLim, chan]
 
        #Calculate interpolation
        b = modXf * br + (1. - modXf) * bl
        t = modXf * tr + (1. - modXf) * tl
        pxf = modYf * t + (1. - modYf) * b
        out.append(int(pxf+0.5))
 
    return out 


def getReplicatedPixel(im, enlargedRImg, n): 

    #enlargedRImg = np.empty(enlargedShape, dtype = np.uint8) 

    for ch in range(im.shape[2]): 
        for r in range(0, im.shape[0]*n - 1): 
            for c in range(0, im.shape[1]*n - 1): 

                # enC = n * ( c - 1 ) + 1
                enC = round( (c-1)*(im.shape[1]-1)/(n*im.shape[1]-1)+1 ) 
                # Finding the location of the col of the original image in the enlarged image 
                enR = round( (r-1)*(im.shape[0]-1)/(n*im.shape[0]-1)+1 )
                # Finding the location of the row of the original image in the enlarged image 

                
                enlargedRImg[r, c, ch] = im[enR, enC, ch]
                # for i in range(0, n): 

                #     # Replicating the neighbouring pixels to the value of the pixel in the original image 
                #     enlargedRImg[enR, enC, ch] = im[r, c, ch] 
                #     enlargedRImg[enR + 1 + i, enC, ch] = im[r, c, ch] 
                #     enlargedRImg[enR, enC + 1 + i, ch] = im[r, c, ch] 
                #     enlargedRImg[enR + 1 + i, enC + 1 + i, ch] = im[r, c, ch] 

    return enlargedRImg 



 
if __name__=="__main__":
    
    im = cv2.imread("./download.jpg", cv2.IMREAD_UNCHANGED) # Reading the image in the BGR format 
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) # Converting from BGR to RGB 
    n = int(input("Enter the zooming factor: ")) # Reading the zooming factor 
    
    # enlargedShape = list(map(int, [im.shape[0]*1.6, im.shape[1]*1.6, im.shape[2]]))
    enlargedShape = list(map(int, [im.shape[0] * n, im.shape[1] * n, im.shape[2]])) 
    
    
    enlargedImg = np.empty(enlargedShape, dtype = np.uint8) 
    enlargedRImg = np.empty(enlargedShape, dtype = np.uint8) 

    rowScale = float(im.shape[0]) / float(enlargedImg.shape[0]) 
    colScale = float(im.shape[1]) / float(enlargedImg.shape[1]) 

    for r in range(enlargedImg.shape[0]):
        for c in range(enlargedImg.shape[1]):
            orir = r * rowScale # Find position in original image
            oric = c * colScale
            enlargedImg[r, c] = GetBilinearPixel(im, oric, orir)
 
     
    
    enlargedRImg = getReplicatedPixel(im, enlargedRImg, n) # Receiving the image from the function getReplicatedPixels 

    # imshow(enlargedImg) 
    # plt.imshow(enlargedImg) 
    img1 = Image.fromarray(enlargedImg, 'RGB') # Saving the Bilinear Interpolated image in the same directory  
    img1.save('./zoomed_imageBI.jpg') 

    img2 = Image.fromarray(enlargedRImg, 'RGB') # Saving the Replicated Pixels Zoomed image in the same directory 
    img2.save('./zoomed_imageR.jpg') 
    # img2.show() 
    print('Zooming completed Successfully')
