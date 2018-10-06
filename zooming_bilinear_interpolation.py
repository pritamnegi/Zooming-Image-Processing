import numpy as np
from scipy.misc import imread, imshow
from scipy import ndimage
import matplotlib.pyplot as plt
import imageio
from PIL import Image
 
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
 
if __name__=="__main__":
 
 	# Insert your file path below
    im = imageio.imread("D:\\My Files\\Zooming DSp\\download.jpg", pilmode="RGB")
    n = int(input("Enter the zooming factor: "))
    enlargedShape = list(map(int, [im.shape[0]*n, im.shape[1]*n, im.shape[2]]))
    enlargedImg = np.empty(enlargedShape, dtype=np.uint8)
    rowScale = float(im.shape[0]) / float(enlargedImg.shape[0])
    colScale = float(im.shape[1]) / float(enlargedImg.shape[1])
 
    for r in range(enlargedImg.shape[0]):
        for c in range(enlargedImg.shape[1]):
            orir = r * rowScale #Find position in original image
            oric = c * colScale
            enlargedImg[r, c] = GetBilinearPixel(im, oric, orir)
 
     # imshow(enlargedImg)
    # plt.imshow(enlargedImg)
    img = Image.fromarray(enlargedImg, 'RGB')
    # Insert your file path below
    img.save('D:\\My Files\\Zooming DSP\\zoomed_image.jpg')
    img.show()