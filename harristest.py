import numpy as np
import cv2
import matplotlib.pyplot as plt
import easygui
   

def Canny_detector(img, weak_th = None, strong_th = None):
      
    # conversion of image to grayscale
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
      
    # noise reduction
    #img = cv2.bilateralFilter(img,9,75,75)
       
    # gradient calculation
    gx = cv2.Sobel(np.float32(img), cv2.CV_64F, 1, 0, 3)
    gy = cv2.Sobel(np.float32(img), cv2.CV_64F, 0, 1, 3)
      
    # converting of cartesian coordinates to polar 
    mag, ang = cv2.cartToPolar(gx, gy, angleInDegrees = True)
       
    
    # setting thresholds for hysterisis thresholding
    mag_max = np.max(mag)
    if not weak_th:weak_th = mag_max * 0.1
    if not strong_th:strong_th = mag_max * 0.5
      
    # getting dimensions of image  
    height, width = img.shape
       
    # looping through every pixel of the image 
    for i_x in range(width):
        for i_y in range(height):
               
            grad_ang = ang[i_y, i_x]
            grad_ang = abs(grad_ang-180) if abs(grad_ang)>180 else abs(grad_ang)
               
            # selecting the neighbours of the target pixel
            # according to the gradient direction
            # In the x axis direction
            if grad_ang<= 22.5:
                neighb_1_x, neighb_1_y = i_x-1, i_y
                neighb_2_x, neighb_2_y = i_x + 1, i_y
              
            # top right (diagonal-1) direction
            elif grad_ang>22.5 and grad_ang<=(22.5 + 45):
                neighb_1_x, neighb_1_y = i_x-1, i_y-1
                neighb_2_x, neighb_2_y = i_x + 1, i_y + 1
              
            # In y-axis direction
            elif grad_ang>(22.5 + 45) and grad_ang<=(22.5 + 90):
                neighb_1_x, neighb_1_y = i_x, i_y-1
                neighb_2_x, neighb_2_y = i_x, i_y + 1
              
            # top left (diagonal-2) direction
            elif grad_ang>(22.5 + 90) and grad_ang<=(22.5 + 135):
                neighb_1_x, neighb_1_y = i_x-1, i_y + 1
                neighb_2_x, neighb_2_y = i_x + 1, i_y-1
              
            # restarting the cycle
            elif grad_ang>(22.5 + 135) and grad_ang<=(22.5 + 180):
                neighb_1_x, neighb_1_y = i_x-1, i_y
                neighb_2_x, neighb_2_y = i_x + 1, i_y
               
            # non-maximum suppression 
            if width>neighb_1_x>= 0 and height>neighb_1_y>= 0:
                if mag[i_y, i_x]<mag[neighb_1_y, neighb_1_x]:
                    mag[i_y, i_x]= 0
                    continue
   
            if width>neighb_2_x>= 0 and height>neighb_2_y>= 0:
                if mag[i_y, i_x]<mag[neighb_2_y, neighb_2_x]:
                    mag[i_y, i_x]= 0
   
    #weak_ids = np.zeros_like(img)
    #strong_ids = np.zeros_like(img)              
    ids = np.zeros_like(img)
       
    # hysterisis thresholding step
    for i_x in range(width):
        for i_y in range(height):
              
            grad_mag = mag[i_y, i_x]
              
            if grad_mag<weak_th:
                mag[i_y, i_x]= 0
            elif strong_th>grad_mag>= weak_th:
                ids[i_y, i_x]= 1
            else:
                ids[i_y, i_x]= 2
       
       
    
    # returning the magnitude of gradients of edges
    return mag

# opening file explorer
file = easygui.fileopenbox()

# loading image
frame = cv2.imread(file)

# conversion of image to grayscale
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
# noise reduction
frame = cv2.bilateralFilter(frame,9,75,75)

# calling canny edge detection function
canny_img = Canny_detector(frame)

# saving canny edge detected image and converting image to float32 datatype
cv2.imwrite('canny1.jpg',canny_img)
canny_img = np.float32(canny_img)

# finding harris corners by using image derivatives and performing mathematical operations on them
harris_img = cv2.cornerHarris(canny_img,2,7,0.07)

# dilating image to mark corners more accurately and superimposing corners on canny edge detected image
harris_img = cv2.dilate(harris_img, None)
can2img = cv2.imread('canny1.jpg')
can2img[harris_img>0.01*harris_img.max()]=[0,0,255]

# displaying image
cv2.imwrite('harris1.jpg',can2img)

finalharris = cv2.imread('harris1.jpg')
 
#f, plots = plt.subplots() 
#plots.imshow(finalharris)
#plt.show()

f, plots = plt.subplots(1, 3) 
plots[0].imshow(frame)
plots[1].imshow(canny_img)
plots[2].imshow(finalharris)
plt.show()