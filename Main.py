#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 02:01:03 2019

@author: earendilavari
"""

# %%%%%%%%%%%%%%%%%% IMPORT USED PACKAGES %%%%%%%%%%%%%%%%%%
import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

exec(open('Camera.py').read())
exec(open('BinaryImg.py').read())

# %%%%%%%%%%%%%%%%%% CAMERA CALIBRATION %%%%%%%%%%%%%%%%%%%%

# Read in and make a list of calibration images
# imagesPath is a list of the names of all calibration images
imagesPath = glob.glob('camera_cal/calibration*.jpg')
# cam is an object of type Camera
cam = Camera()
# The camera matrix and the coeficients are calculated 
matrix, dist = cam.Calibrate(imagesPath, 9, 6)
distortedImgTest = mpimg.imread('camera_cal/calibration1.jpg')
undistortedImgTest = cam.UndistortImage(distortedImgTest, matrix, dist)

# Plot the distorted and undistorted test image
figure1, fig1_axes = plt.subplots(1,2, figsize=(10,5))
figure1.tight_layout()
figure1.suptitle('Calibration image used. Before and after calibration')
fig1_axes[0].imshow(distortedImgTest)
fig1_axes[0].set_title('Distorted Image', fontsize = 10)
fig1_axes[1].imshow(undistortedImgTest)
fig1_axes[1].set_title('Undistorted Image', fontsize = 10)
plt.subplots_adjust(top = 1.1, bottom = 0)
figure1.savefig('ImgsReport/01_CalibImgAfterUndistort')

undistortedImgsSavePath = 'camera_cal/Undistorted/calibration%i.jpg'
cam.UndistortAndSaveImageList(imagesPath, matrix, dist, undistortedImgsSavePath)

### By plotting both images (undistorted and distorted) it can be seen how the undistorting processing
### worked on the camera. In the case of this camera, the original images are not that distorted, only in the 
### edges a convex distortion can be seen, which is corrected on the undistorted image.

# %%%%%%%%%%%%%%%%%% UNDISTORT A TEST IMAGE %%%%%%%%%%%%%%%%%%

# Now that the camera matrix and the calibration coeficients are calculated, they can be used to undistort one
# of the test images

# Let's try it with "straight_lines1.jpg'. This image will be used further for the development of the pipeline

# Reads the test image
imgStraightLines1 = mpimg.imread('test_images/straight_lines1.jpg')
imgStraightLines1Undist = cam.UndistortImage(imgStraightLines1, matrix, dist)

# Plot both images
figure2, fig2_axes = plt.subplots(1,2, figsize=(10,5))
figure2.tight_layout()
figure2.suptitle('Image "straight_lines1.jpg" before and after calibration')
fig2_axes[0].imshow(imgStraightLines1)
fig2_axes[0].set_title('Distorted Image', fontsize = 10)
fig2_axes[1].imshow(imgStraightLines1Undist)
fig2_axes[1].set_title('Undistorted Image', fontsize = 10)
plt.subplots_adjust(top = 1.1, bottom = 0)
figure2.savefig('ImgsReport/02_straight_lines1_beforeAndAfterCalib')

### By plotting this test image it can be seen that a little bit of the original image is missing on the 
### undistorted image. Also some objects are bigger, but the difference is actually minimal.

#%% Let's try it with 'test1.jpg' now.

# Reads the test image
imgTest1 = mpimg.imread('test_images/test1.jpg')
imgTest1Undist = cam.UndistortImage(imgTest1, matrix, dist)
figure3, fig3_axes = plt.subplots(1,2, figsize=(10,5))
figure3.tight_layout()
figure3.suptitle('Image "test1.jpg" before and after calibration')
fig3_axes[0].imshow(imgTest1)
fig3_axes[0].set_title('Distorted Image', fontsize = 10)
fig3_axes[1].imshow(imgTest1Undist)
fig3_axes[1].set_title('Undistorted Image', fontsize = 10)
plt.subplots_adjust(top = 1.1, bottom = 0)
figure3.savefig('ImgsReport/03_test1_beforeAndAfterCalib')

### On this image it can be seen again how in the undistorted image, the contents on the borders of the 
### images is missing and some objects are bigger.

# %%%%%%%%%%%%%%%%%% BINARY IMAGE FOR LINE DETECTION %%%%%%%%%%%%%%%%%%%%

'''
To create binary images, the class BinaryImg was created with the function GradientCalc. 
This function can create binary images in all the possible cases seen in the lessons. 

It can convert the image into grayscale, HSL or HSV. From it, it can calculate the gradient in the X direction, in the Y direction,
its magnitude or its direction. If the image is converted to HSL or HSV, one of the channels need to be selected.

By using this function, it can be easily compared between the different methods in order to get a binary image.

'''

# Lets create an object of type BinaryImg
binImg = BinaryImg()

# Now lets try the function for directionX, directionY and magnitude using a grayscale image. That will be done
# using the image 'straight_lines1.png' after being undistorted

strLines1BinGrayDirX = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'grayscale', calcType = 'dirX', thresh = (40, 120))
strLines1BinGrayDirY = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'grayscale', calcType = 'dirY', thresh = (40, 120))
strLines1BinGrayMag = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'grayscale', calcType = 'magnitude', thresh = (40, 120))

figure4, fig4_axes = plt.subplots(2,2, figsize = (10, 8))
figure4.tight_layout()
figure4.suptitle('Binary images created with grayscale image and gradient. Threshold = (40, 120)')
fig4_axes[0, 0].imshow(imgStraightLines1Undist)
fig4_axes[0, 0].set_title('Original Image')
fig4_axes[0, 1].imshow(strLines1BinGrayDirX, cmap = 'gray')
fig4_axes[0, 1].set_title('Binary Grayscale with gradient in X direction')
fig4_axes[1, 0].imshow(strLines1BinGrayDirY, cmap = 'gray')
fig4_axes[1, 0].set_title('Binary Grayscale with gradient in Y direction')
fig4_axes[1, 1].imshow(strLines1BinGrayMag, cmap = 'gray')
fig4_axes[1, 1].set_title('Binary Grayscale with magnitude of gradient')
figure4.savefig('ImgsReport/04_BinImgsGrayGradient')


'''
By showing all three images can be seen that the lines are better shown on the binary image created by taking the gradient in the X
direction. The difference is not that big though. Also, if the threshold is increased, the rest of the scenery disapears before the
lines, because the lines have a more strong gradient.
'''

# %% Let's create now a new binary image calculating the direction of the gradient 

strLines1BinGrayDir = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'grayscale', calcType = 'direction', thresh = (0.8, 1.2))

figure5, fig5_axes = plt.subplots(1, 2, figsize = (10, 5))
figure5.tight_layout()
figure5.suptitle('Binary images created with grayscale image and gradient direction. \nThreshold = (0.7 rad, 1.3 rad)')
fig5_axes[0].imshow(imgStraightLines1Undist)
fig5_axes[0].set_title('Original Image')
fig5_axes[1].imshow(strLines1BinGrayDir, cmap = 'gray')
fig5_axes[1].set_title('Binary Grayscale with direction of gradient')
figure5.savefig('ImgsReport/05_BinImgsGrayGradientDir')

'''
The binary image created by calculating the direction of the gradient shows a lot of noise, but with very good defined lines. For now 
we will discard this result, but it may be usefull in the future.
'''

# %% Now let's see what we get by using HSL color space

strLines1BinHSLchHDirX = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'h', calcType = 'dirX', thresh = (40, 120))
strLines1BinHSLchHDirY = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'h', calcType = 'dirY', thresh = (40, 120))
strLines1BinHSLchHMag = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'h', calcType = 'magnitude', thresh = (40, 120))
strLines1BinHSLchSDirX = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 's', calcType = 'dirX', thresh = (40, 120))
strLines1BinHSLchSDirY = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 's', calcType = 'dirY', thresh = (40, 120))
strLines1BinHSLchSMag = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 's', calcType = 'magnitude', thresh = (40, 120))
strLines1BinHSLchLDirX = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (40, 120))
strLines1BinHSLchLDirY = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'l', calcType = 'dirY', thresh = (40, 120))
strLines1BinHSLchLMag = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'l', calcType = 'magnitude', thresh = (40, 120))

figure6, fig6_axes = plt.subplots(3,3, figsize = (11.5, 11))
figure6.tight_layout()
figure6.suptitle('Binary images created with HSL color space and gradient. Threshold = (40, 120)')
fig6_axes[0,0].imshow(strLines1BinHSLchHDirX, cmap = 'gray')
fig6_axes[0,0].set_title('Channel H, Direction X', fontsize = 10)
fig6_axes[0,1].imshow(strLines1BinHSLchHDirY, cmap = 'gray')
fig6_axes[0,1].set_title('Channel H, Direction Y', fontsize = 10)
fig6_axes[0,2].imshow(strLines1BinHSLchHMag, cmap = 'gray')
fig6_axes[0,2].set_title('Channel H, Magnitude', fontsize = 10)
fig6_axes[1,0].imshow(strLines1BinHSLchSDirX, cmap = 'gray')
fig6_axes[1,0].set_title('Channel S, Direction X', fontsize = 10)
fig6_axes[1,1].imshow(strLines1BinHSLchSDirY, cmap = 'gray')
fig6_axes[1,1].set_title('Channel S, Direction Y', fontsize = 10)
fig6_axes[1,2].imshow(strLines1BinHSLchSMag, cmap = 'gray')
fig6_axes[1,2].set_title('Channel S, Magnitude', fontsize = 10)
fig6_axes[2,0].imshow(strLines1BinHSLchLDirX, cmap = 'gray')
fig6_axes[2,0].set_title('Channel L, Direction X', fontsize = 10)
fig6_axes[2,1].imshow(strLines1BinHSLchLDirY, cmap = 'gray')
fig6_axes[2,1].set_title('Channel L, Direction Y', fontsize = 10)
fig6_axes[2,2].imshow(strLines1BinHSLchLMag, cmap = 'gray')
fig6_axes[2,2].set_title('Channel L, Magnitude', fontsize = 10)
plt.subplots_adjust(top = 0.9, bottom = 0.1)
figure6.savefig('ImgsReport/06_BinImgsHSLGradient')

'''
By showing all the images received can be seen that the channel H is not usefull to draw the lines into the binary images, In it a lof of scenery is detected
but the lines not. The channel S does a very good job by detecting the lines, but they are missing sometimes. There is not a big difference between taking 
the gradient in direction x, y or the magnitude.
On the other hand, the channel L does even a better job than the channel S by detecting the lines, but it also detects some scenery. It must be remembered that
all that scenery will not be considered when the line pixels will be detected and calculated, so it could be safely said that the L channel is here the best 
option to detect the lines. 
'''

# %% Only to try, lets see what we get with the same settings but another theshold range

strLines1BinHSLchHDirX = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'h', calcType = 'dirX', thresh = (30, 150))
strLines1BinHSLchHDirY = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'h', calcType = 'dirY', thresh = (30, 150))
strLines1BinHSLchHMag = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'h', calcType = 'magnitude', thresh = (30, 150))
strLines1BinHSLchSDirX = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 's', calcType = 'dirX', thresh = (30, 150))
strLines1BinHSLchSDirY = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 's', calcType = 'dirY', thresh = (30, 150))
strLines1BinHSLchSMag = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 's', calcType = 'magnitude', thresh = (30, 150))
strLines1BinHSLchLDirX = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (30, 150))
strLines1BinHSLchLDirY = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'l', calcType = 'dirY', thresh = (30, 150))
strLines1BinHSLchLMag = binImg.GradientCalc(imgStraightLines1Undist, imgType = 'HSL', imgChannel = 'l', calcType = 'magnitude', thresh = (30, 150))

figure7, fig7_axes = plt.subplots(3,3, figsize = (11.5, 11))
figure7.tight_layout()
figure7.suptitle('Binary images created with HSL color space and gradient. Threshold = (30, 150)')
fig7_axes[0,0].imshow(strLines1BinHSLchHDirX, cmap = 'gray')
fig7_axes[0,0].set_title('Channel H, Direction X', fontsize = 10)
fig7_axes[0,1].imshow(strLines1BinHSLchHDirY, cmap = 'gray')
fig7_axes[0,1].set_title('Channel H, Direction Y', fontsize = 10)
fig7_axes[0,2].imshow(strLines1BinHSLchHMag, cmap = 'gray')
fig7_axes[0,2].set_title('Channel H, Magnitude', fontsize = 10)
fig7_axes[1,0].imshow(strLines1BinHSLchSDirX, cmap = 'gray')
fig7_axes[1,0].set_title('Channel S, Direction X', fontsize = 10)
fig7_axes[1,1].imshow(strLines1BinHSLchSDirY, cmap = 'gray')
fig7_axes[1,1].set_title('Channel S, Direction Y', fontsize = 10)
fig7_axes[1,2].imshow(strLines1BinHSLchSMag, cmap = 'gray')
fig7_axes[1,2].set_title('Channel S, Magnitude', fontsize = 10)
fig7_axes[2,0].imshow(strLines1BinHSLchLDirX, cmap = 'gray')
fig7_axes[2,0].set_title('Channel L, Direction X', fontsize = 10)
fig7_axes[2,1].imshow(strLines1BinHSLchLDirY, cmap = 'gray')
fig7_axes[2,1].set_title('Channel L, Direction Y', fontsize = 10)
fig7_axes[2,2].imshow(strLines1BinHSLchLMag, cmap = 'gray')
fig7_axes[2,2].set_title('Channel L, Magnitude', fontsize = 10)
plt.subplots_adjust(top = 0.9, bottom = 0.1)
figure7.savefig('ImgsReport/07_BinImgsHSLGradientOtherThreshold')

'''
By increasing the threshold range, it gets more evident that the Channel L, with the gradient in the X direction is the best approach to detect the lines. 
They are drawn very clear and with not that many other irrelevant elements. The binary images created with the channel S are still missing some parts of the 
line.

This can be explained by thinking how the colorspace HSL works. The H component (Hue) corresponds to the value of the base color 
(red, green, blue, cyan, magenta and yellow), the S component (Saturation) corresponds to the strength of the shown color, and the L (Lightness) corresponds to
how close the color is to white. Since the lane lines are normally white or light yellow, they are more easy to detect using the L component because they are 
very close to white. But what if the line is darker yellow? In that case the channel L can fail to detect the lane lines, but in the channel S, they will still 
be strong enough.
'''

# %% Lets visualize the last idea about the HSL colorspace by ploting the same image in their HSL components

imgStraightLines1UndistHSL = cv2.cvtColor(imgStraightLines1Undist, cv2.COLOR_RGB2HLS)

figure8, fig8_axes = plt.subplots(2,2, figsize = (10, 5))
figure8.tight_layout()
figure8.suptitle('Image "straight_lines1.jpg" and its HSL components')
fig8_axes[0,0].imshow(imgStraightLines1Undist)
fig8_axes[0,0].set_title('Original image', fontsize = 10)
fig8_axes[0,1].imshow(imgStraightLines1UndistHSL[:,:,0], cmap = 'gray')
fig8_axes[0,1].set_title('Component H', fontsize = 10)
fig8_axes[1,0].imshow(imgStraightLines1UndistHSL[:,:,1], cmap = 'gray')
fig8_axes[1,0].set_title('Component L', fontsize = 10)
fig8_axes[1,1].imshow(imgStraightLines1UndistHSL[:,:,2], cmap = 'gray')
fig8_axes[1,1].set_title('Component S', fontsize = 10)
plt.subplots_adjust(top = 0.9, bottom = 0.05)
figure8.savefig('ImgsReport/08_imgStraightLinesHSLGray')

'''
By showing the HSL components of the image, it can be seen that in the S component, the lines are very easy to see, without applying some
gradient, it seem like a good idea to create a binary image with this component
'''

# %% Binary image with HSL components

imgStrLin1UndistH_bin = binImg.HSLBinary(imgStraightLines1Undist, 'h', (180, 255))
imgStrLin1UndistS_bin = binImg.HSLBinary(imgStraightLines1Undist, 's', (180, 255))
imgStrLin1UndistL_bin = binImg.HSLBinary(imgStraightLines1Undist, 'l', (180, 255))

figure9, fig9_axes = plt.subplots(2,2, figsize = (10, 5))
figure9.tight_layout()
figure9.suptitle('Image "straight_lines1.jpg" and binary HSL components. Threshold = (150, 255)')
fig9_axes[0,0].imshow(imgStraightLines1Undist)
fig9_axes[0,0].set_title('Original image', fontsize = 10)
fig9_axes[0,1].imshow(imgStrLin1UndistH_bin, cmap = 'gray')
fig9_axes[0,1].set_title('Component H', fontsize = 10)
fig9_axes[1,0].imshow(imgStrLin1UndistL_bin, cmap = 'gray')
fig9_axes[1,0].set_title('Component L', fontsize = 10)
fig9_axes[1,1].imshow(imgStrLin1UndistS_bin, cmap = 'gray')
fig9_axes[1,1].set_title('Component S', fontsize = 10)
plt.subplots_adjust(top = 0.9, bottom = 0.05)
figure9.savefig('ImgsReport/09_imgStraightLinesHSLBin')

'''
By showing the binary images created thresholding the HSL components can be seen how good the lines are detected by the L and S components. 
The L component finds still more pieces of the line, but also another parts of the image, so it would not be smart to use it as it is without
applying gradient. Specially when the light is very strong, the L component could be very high everywhere, disturbing the line measurements
a lot. In the S component with the selected threshold almost only the lines can be seen, so it seems viable to use it to detect the lines.
'''

# %% Let's now identify the lines within all the other seven given test images

imgStraight_lines2 = mpimg.imread('test_images/straight_lines2.jpg')
imgTest1 = mpimg.imread('test_images/test1.jpg')
imgTest2 = mpimg.imread('test_images/test2.jpg')
imgTest3 = mpimg.imread('test_images/test3.jpg')
imgTest4 = mpimg.imread('test_images/test4.jpg')
imgTest5 = mpimg.imread('test_images/test5.jpg')
imgTest6 = mpimg.imread('test_images/test6.jpg')

# First they need to be undistorted
imgStraight_lines2ud = cam.UndistortImage(imgStraight_lines2, matrix, dist)
imgTest1ud = cam.UndistortImage(imgTest1, matrix, dist)
imgTest2ud = cam.UndistortImage(imgTest2, matrix, dist)
imgTest3ud = cam.UndistortImage(imgTest3, matrix, dist)
imgTest4ud = cam.UndistortImage(imgTest4, matrix, dist)
imgTest5ud = cam.UndistortImage(imgTest5, matrix, dist)
imgTest6ud = cam.UndistortImage(imgTest6, matrix, dist)

# Then their binary images created with the gradient in direction X using the component L
imgStraight_lines2_Lgrad = binImg.GradientCalc(imgStraight_lines2ud, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 190))
imgTest1_Lgrad = binImg.GradientCalc(imgTest1ud, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))
imgTest2_Lgrad = binImg.GradientCalc(imgTest2ud, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))
imgTest3_Lgrad = binImg.GradientCalc(imgTest3ud, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))
imgTest4_Lgrad = binImg.GradientCalc(imgTest4ud, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))
imgTest5_Lgrad = binImg.GradientCalc(imgTest5ud, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))
imgTest6_Lgrad = binImg.GradientCalc(imgTest6ud, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))

# And the binary images created with the S component
imgStraight_lines2_S = binImg.HSLBinary(imgStraight_lines2ud, 's', (180, 255))
imgTest1_S = binImg.HSLBinary(imgTest1ud, 's', (180, 250))
imgTest2_S = binImg.HSLBinary(imgTest2ud, 's', (180, 250))
imgTest3_S = binImg.HSLBinary(imgTest3ud, 's', (180, 250))
imgTest4_S = binImg.HSLBinary(imgTest4ud, 's', (180, 250))
imgTest5_S = binImg.HSLBinary(imgTest5ud, 's', (180, 250))
imgTest6_S = binImg.HSLBinary(imgTest6ud, 's', (180, 250))


# Finally, lets combine the images in bicolor images, in order to see which parts are selected by the gradient of the L component and which parts are
# selected by the S component
imgStraight_lines2_bin = binImg.CombineBinariesBlueGreen(imgStraight_lines2_Lgrad, imgStraight_lines2_S)
imgTest1_bin = binImg.CombineBinariesBlueGreen(imgTest1_Lgrad, imgTest1_S)
imgTest2_bin = binImg.CombineBinariesBlueGreen(imgTest2_Lgrad, imgTest2_S)
imgTest3_bin = binImg.CombineBinariesBlueGreen(imgTest3_Lgrad, imgTest3_S)
imgTest4_bin = binImg.CombineBinariesBlueGreen(imgTest4_Lgrad, imgTest4_S)
imgTest5_bin = binImg.CombineBinariesBlueGreen(imgTest5_Lgrad, imgTest5_S)
imgTest6_bin = binImg.CombineBinariesBlueGreen(imgTest6_Lgrad, imgTest6_S)

# And plot them
figure10, fig10_axes = plt.subplots(3,2, figsize = (11, 11))
figure10.tight_layout()
figure10.suptitle('Binary images with gradient in X direction of the component L in green and clean component S in blue. \n Threshold gradient L = (30, 150), Threshold S = (150, 255)')
fig10_axes[0,0].imshow(imgStraight_lines2)
fig10_axes[0,0].set_title('"straight_lines2.jpg"', fontsize = 10)
fig10_axes[0,0].axis('off')
fig10_axes[0,1].imshow(imgStraight_lines2_bin)
fig10_axes[0,1].set_title('Binary "straight_lines2.jpg"', fontsize = 10)
fig10_axes[0,1].axis('off')
fig10_axes[1,0].imshow(imgTest1)
fig10_axes[1,0].set_title('"test1.jpg"', fontsize = 10)
fig10_axes[1,0].axis('off')
fig10_axes[1,1].imshow(imgTest1_bin)
fig10_axes[1,1].set_title('Binary "test1.jpg"', fontsize = 10)
fig10_axes[1,1].axis('off')
fig10_axes[2,0].imshow(imgTest2)
fig10_axes[2,0].set_title('"test2.jpg"', fontsize = 10)
fig10_axes[2,0].axis('off')
fig10_axes[2,1].imshow(imgTest2_bin)
fig10_axes[2,1].set_title('Binary "test2.jpg"', fontsize = 10)
fig10_axes[2,1].axis('off')
plt.subplots_adjust(top = 0.9, bottom = 0.05)
figure10.savefig('ImgsReport/10_AllTestImagesBin01')

figure11, fig11_axes = plt.subplots(3,2, figsize = (11, 11))
figure11.tight_layout()
figure11.suptitle('Binary images with gradient in X direction of the component L in green and clean component S in blue. \n Threshold gradient L = (30, 150), Threshold S = (150, 255)')
fig11_axes[0,0].imshow(imgTest3)
fig11_axes[0,0].set_title('"test3.jpg"', fontsize = 10)
fig11_axes[0,0].axis('off')
fig11_axes[0,1].imshow(imgTest3_bin)
fig11_axes[0,1].set_title('Binary "test3.jpg"', fontsize = 10)
fig11_axes[0,1].axis('off')
fig11_axes[1,0].imshow(imgTest4)
fig11_axes[1,0].set_title('"test4.jpg"', fontsize = 10)
fig11_axes[1,0].axis('off')
fig11_axes[1,1].imshow(imgTest4_bin)
fig11_axes[1,1].set_title('Binary "test4.jpg"', fontsize = 10)
fig11_axes[1,1].axis('off')
fig11_axes[2,0].imshow(imgTest5)
fig11_axes[2,0].set_title('"test5.jpg"', fontsize = 10)
fig11_axes[2,0].axis('off')
fig11_axes[2,1].imshow(imgTest5_bin)
fig11_axes[2,1].set_title('Binary "test5.jpg"', fontsize = 10)
fig11_axes[2,1].axis('off')
plt.subplots_adjust(top = 0.9, bottom = 0.05)
figure11.savefig('ImgsReport/11_AllTestImagesBin02')


'''
By applying both methods on all images, can be seen that the combination of both is a very good approach to get the lane lines. What 
does not get detected by the gradient in direction X of the L component, gets detected with the S component and viceversa. 
This method will be used to get the lane line points and after that the equations corresponding to the lane lines.

A little optimization was here done with the parameters, the threshold range for the gradient in X was changed from (30, 150) to (35. 175)
and the threshold range for the S component was changed from (180, 255) to (180, 250) in order to prevent very strong shadows to appear 
in the binary image, like in "test5.jpg"
'''

# %%%%%%%%%%%%%%%%%%% PERSPECTIVE TRANSFORM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

'''
Now that we have a robust method to get a binary image where the line pixels can be found, it is time to transform the images into
an aereal view, so the lines can be seen in a plane.
For that, the function WarpPolygonToSquare was added to the Camera class. It transforms the image using a polygon, so it receives four values
of X and two of Y.

Let's try that function with the first image "straight_lines1.jpg"
'''

imgStraightLines1Warped = cam.WarpPolygonToSquare(imgStraightLines1Undist, 450, 700, 200, 580, 1100, 700)

# Now, lets print it and compare it with the original image

figure12, fig12_axes = plt.subplots(1, 2, figsize = (10, 5))
figure12.tight_layout()
figure12.suptitle('Perspective transformed image')
fig12_axes[0].imshow(imgStraightLines1Undist)
fig12_axes[0].set_title('Original Image')
fig12_axes[1].imshow(imgStraightLines1Warped)
fig12_axes[1].set_title('Transformed image')
figure12.savefig('ImgsReport/12_StraightLines1_transformed')

'''
As it can be seen in the images, the perspective transform is working well getting an image in "bird view" perspective. The problem is
that the lines are not paralel as they should be. That is because the vertices of the selected polygon were selected very roughly. That the 
lines are paralel in the bird view image is very important in order to get good calculations after that. So it is needed to get the vertices
of that polygon in a precise way.

Here is where the work in the first project can be very useful to calculate those vertices. So we import from the first project functions 
"region_of_interest", "hough_vertices" and "hough_lines", now located in the file HoughLines.py and we update the "hough_lines" function to 
return the points at the beginning and at the end of the line.

Also the function "CombineBinaries" was added to the class BinaryImg. 
'''

# %%%%%%%%%%%%%%%%%%% PERSPECTIVE TRANSFORM WITH HOUGH LINES %%%%%%%%%%%%%%%%%%

exec(open('HoughLines.py').read())

# First, the binary image where the lane lines are visible needs to be made, to do that, the two images calculated before are used
imgStraightLines1bin =  binImg.CombineBinaries(strLines1BinHSLchLDirX, imgStrLin1UndistS_bin)

# Now the vertices where we calculate the Hough lines
y_horizon = 465
y_bottom = imgStraightLines1bin.shape[0] - 50

houghVertices = houghVertices(100, 550, 1200, 800, y_bottom, y_horizon)

# Then crop the image to the region of interest
houghRegion = region_of_interest(imgStraightLines1bin, houghVertices)

# Then calculate the hough lines, together with the points
houghLines, x_bottomLeft, x_topLeft, x_bottomRight, x_topRight = hough_lines(imgStraightLines1Undist, imgStraightLines1bin, 
                                                                                 1, np.pi/180, 50, 40, 2, y_horizon)
# Now with the new points the warped image corrected
imgStraightLines1Warped_corr = cam.WarpPolygonToSquare(imgStraightLines1Undist, y_horizon, imgStraightLines1Undist.shape[0], 
                                                       x_bottomLeft, x_topLeft, x_bottomRight, x_topRight)

# Lets draw the polygon in the original image
polygonVerticesOrig = np.array([[x_bottomLeft, y_bottom + 50],[x_topLeft, y_horizon],[x_topRight, y_horizon],[x_bottomRight, y_bottom + 50]], 
                           np.int32)
polygonVerticesWarped = np.array([[300, imgStraightLines1Warped_corr.shape[0]], [300, 0], [imgStraightLines1Warped_corr.shape[1] - 300, 0], 
                                  [imgStraightLines1Warped_corr.shape[1] - 300, imgStraightLines1Warped_corr.shape[0]]], np.int32)

imgStraightLines1Poly = imgStraightLines1Undist.copy()
imgStraightLines1Warped_corrPoly = imgStraightLines1Warped_corr.copy()
cv2.polylines(imgStraightLines1Poly, [polygonVerticesOrig], True, (255,0,0),3)
cv2.polylines(imgStraightLines1Warped_corrPoly, [polygonVerticesWarped], True, (255,0,0),4)

# Now let's print the entire process
figure13, fig13_axes = plt.subplots(2,2, figsize = (10, 5))
figure13.tight_layout()
figure13.suptitle('Perspective transformed image using polygon calculated with Hough lane lines')
fig13_axes[0,0].imshow(houghRegion, cmap = 'gray')
fig13_axes[0,0].set_title('Binary image masked with a region of interest', fontsize = 10)
fig13_axes[0,1].imshow(houghLines)
fig13_axes[0,1].set_title('Lane lines detected with Hough Lines Algorithm', fontsize = 10)
fig13_axes[1,0].imshow(imgStraightLines1Poly)
fig13_axes[1,0].set_title('Original image with transformation polygon', fontsize = 10)
fig13_axes[1,1].imshow(imgStraightLines1Warped_corrPoly)
fig13_axes[1,1].set_title('Transformated image', fontsize = 10)
plt.subplots_adjust(top = 0.9, bottom = 0.05)
figure13.savefig('ImgsReport/13_StraightLines1_transformed_corr')

'''
By using this method to find the vertices of the conversion polygon the lane lines in the converted image are completely paralel. What means
that the conversion is now accurate and appropiate to be used. The best thing is, that this process is not needed in the pipeline, these 
vertices can be used for any image to convert it into bird view image, so they can be used as parameters within the pipeline.
'''

# %% Lets validate the parameters by doing the conversion with other three images

imgTest1_warped = cam.WarpPolygonToSquare(imgTest1ud, y_horizon, imgTest1ud.shape[0], 
                                        x_bottomLeft, x_topLeft, x_bottomRight, x_topRight)

imgTest2_warped = cam.WarpPolygonToSquare(imgTest2ud, y_horizon, imgTest2ud.shape[0], 
                                        x_bottomLeft, x_topLeft, x_bottomRight, x_topRight)

imgTest3_warped = cam.WarpPolygonToSquare(imgTest3ud, y_horizon, imgTest3ud.shape[0], 
                                        x_bottomLeft, x_topLeft, x_bottomRight, x_topRight)

figure14, fig14_axes = plt.subplots(3,2, figsize = (11, 11))
figure14.tight_layout()
figure14.suptitle('Perspective transformed images using polygon calculated with Hough lane lines')
fig14_axes[0,0].imshow(imgTest1ud)
fig14_axes[0,0].set_title('"test1.jpg"', fontsize = 10)
fig14_axes[0,0].axis('off')
fig14_axes[0,1].imshow(imgTest1_warped)
fig14_axes[0,1].set_title('Warped "test1.jpg"', fontsize = 10)
fig14_axes[0,1].axis('off')
fig14_axes[1,0].imshow(imgTest2ud)
fig14_axes[1,0].set_title('"test2.jpg"', fontsize = 10)
fig14_axes[1,0].axis('off')
fig14_axes[1,1].imshow(imgTest2_warped)
fig14_axes[1,1].set_title('Warped "test2.jpg"', fontsize = 10)
fig14_axes[1,1].axis('off')
fig14_axes[2,0].imshow(imgTest3ud)
fig14_axes[2,0].set_title('"test3.jpg"', fontsize = 10)
fig14_axes[2,0].axis('off')
fig14_axes[2,1].imshow(imgTest3_warped)
fig14_axes[2,1].set_title('Warped "test5.jpg"', fontsize = 10)
fig14_axes[2,1].axis('off')
plt.subplots_adjust(top = 0.9, bottom = 0.05)
figure14.savefig('ImgsReport/14_TestImagesWarped')

'''
By showing the three images and their warped version it can be seen how well this polygon does performing the transformation. In all the three
images the lines stay paralel, which means that the conversion is valid and can be used for further analysis.
'''

# %%%%%%%%%%%%%%%%%%% BINARY IMAGE AND PERSPECTIVE TRANSFORM %%%%%%%%%%%%%%%%%%%%%%%%

'''
Now that the methods to get a binary image and to warp it into a bird view image are selected, programmed and tested with test images, it is 
important to decide: What to do first? get the binary image and then the perspective transform or viceversa?. For that, binary transformed 
images of some of the test images in both orders will be created to see which order is better.
'''

## First binary image, than perspective transform

imgTest1_bin = binImg.CombineBinaries(imgTest1_Lgrad, imgTest1_S)
imgTest2_bin = binImg.CombineBinaries(imgTest2_Lgrad, imgTest2_S)
imgTest3_bin = binImg.CombineBinaries(imgTest3_Lgrad, imgTest3_S)

imgTest1_binWarped = cam.WarpPolygonToSquare(imgTest1_bin, y_horizon, imgTest1ud.shape[0], 
                                        x_bottomLeft, x_topLeft, x_bottomRight, x_topRight)

imgTest2_binWarped = cam.WarpPolygonToSquare(imgTest2_bin, y_horizon, imgTest1ud.shape[0], 
                                        x_bottomLeft, x_topLeft, x_bottomRight, x_topRight)

imgTest3_binWarped = cam.WarpPolygonToSquare(imgTest3_bin, y_horizon, imgTest1ud.shape[0], 
                                        x_bottomLeft, x_topLeft, x_bottomRight, x_topRight)


## First perspective transform, than binary image

imgTest1_warpedLgrad = binImg.GradientCalc(imgTest1_warped, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))
imgTest2_warpedLgrad = binImg.GradientCalc(imgTest2_warped, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))
imgTest3_warpedLgrad = binImg.GradientCalc(imgTest3_warped, imgType = 'HSL', imgChannel = 'l', calcType = 'dirX', thresh = (35, 160))

imgTest1_warpedS = binImg.HSLBinary(imgTest1_warped, 's', (180, 250))
imgTest2_warpedS = binImg.HSLBinary(imgTest2_warped, 's', (180, 250))
imgTest3_warpedS = binImg.HSLBinary(imgTest3_warped, 's', (180, 250))

imgTest1_warpedBin = binImg.CombineBinaries(imgTest1_warpedLgrad, imgTest1_warpedS)
imgTest2_warpedBin = binImg.CombineBinaries(imgTest2_warpedLgrad, imgTest2_warpedS)
imgTest3_warpedBin = binImg.CombineBinaries(imgTest3_warpedLgrad, imgTest3_warpedS)

## Let's plot the first image
figure15, fig15_axes = plt.subplots(2,2, figsize = (10, 5))
figure15.tight_layout()
figure15.suptitle('Get binary image and then warp vs warp and then get binary image for "test2.jpg"')
fig15_axes[0,0].imshow(imgTest2ud)
fig15_axes[0,0].set_title('Original image', fontsize = 10)
fig15_axes[0,1].imshow(imgTest2_warped)
fig15_axes[0,1].set_title('Warped image', fontsize = 10)
fig15_axes[1,0].imshow(imgTest2_binWarped, cmap = 'gray')
fig15_axes[1,0].set_title('Binary and then warped', fontsize = 10)
fig15_axes[1,1].imshow(imgTest2_warpedBin, cmap = 'gray')
fig15_axes[1,1].set_title('Warped and then binary', fontsize = 10)
plt.subplots_adjust(top = 0.9, bottom = 0.05)
figure15.savefig('ImgsReport/15_ComparisonOrderTest2')

'''
For this image can be seen that both results are very similar, but in the warped image before getting the binary image with the lines
the right dashed line is not so well defined, also a little detail in the road is stronger detected in that version. Another thing is the 
car. While by creating first the binary image and then warping it the car does not get detected, but by warping the image and then creating
a binary image from it, the car gets detected, what can cause wrong measurements of the lines.

Let's plot the comparison with another image to be sure what option is the best
'''

# %% 

## Let's plot the first image
figure16, fig16_axes = plt.subplots(2,2, figsize = (10, 5))
figure16.tight_layout()
figure16.suptitle('Get binary image and then warp vs warp and then get binary image for "test1.jpg"')
fig16_axes[0,0].imshow(imgTest1ud)
fig16_axes[0,0].set_title('Original image', fontsize = 10)
fig16_axes[0,1].imshow(imgTest1_warped)
fig16_axes[0,1].set_title('Warped image', fontsize = 10)
fig16_axes[1,0].imshow(imgTest1_binWarped, cmap = 'gray')
fig16_axes[1,0].set_title('Binary and then warped', fontsize = 10)
fig16_axes[1,1].imshow(imgTest1_warpedBin, cmap = 'gray')
fig16_axes[1,1].set_title('Warped and then binary', fontsize = 10)
plt.subplots_adjust(top = 0.9, bottom = 0.05)
figure16.savefig('ImgsReport/16_ComparisonOrderTest1')


'''
In the case of this image, it can be seen that the left line gets detected longer in the version where first the binary image is created 
and then the binary image is warped than in the contrary version. Also in the contrary version some other details of the street are being
detected, which are not part of the line. So the better approach may be to get first the binary image and then warp it.
'''

# %%%%%%%%%%%%%%%%%%%%%%%%%% IDENTIFICATION OF LANE LINE PIXELS ON WARPED BINARY IMAGE %%%%%%%%%%%%%%%%%


