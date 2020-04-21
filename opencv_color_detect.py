import cv2
import numpy as np

BLUR=(5,5)
threshold=0
#set BGR color thresholds
THRESH_TXT=["Blue", "Green"]
THRESH_LOW=[[80,40,0],[40,80,0]]
THRESH_HI=[[220,100,80], [100,220,80]]

#process_image() produces 4 different images 
def process_image(raw_image, control):
    global threshold
    text=[]
    images=[]
    
    #switch color threshold either blue or green 
    if control== ord("c"):
        threshold=(threshold+1)%len(THRESH_LOW)
    

        
    #save and display a copy of raw image
    text.append("Raw Image %s"%THRESH_TXT[threshold])
    images.append(raw_image)
    
    #blur and display raw image to decrease noise in image
    text.append("Blur %s caption"%THRESH_TXT[threshold])
    images.append(cv2.blur(raw_image, BLUR))
    
    
    #set color thresholds respective to COLOR
    lower= np.array(THRESH_LOW[threshold], dtype="uint8")
    upper= np.array(THRESH_HI[threshold], dtype="uint8")
    
    #apply thresholds and display black and white image 
    text.append("Threshold %s caption"%THRESH_TXT[threshold])
    images.append(cv2.inRange(images[-1],lower, upper))
    
     
    #Output contours from the threshold image
    text.append("Contours %s caption"%THRESH_TXT[threshold])
    images.append(images[-1].copy())
    #cv2.findContours() returns in a list all the contours in the threshold image
    #every element of the list contours is an array of (x,y) coordinates
    image, contours, hierarchy=cv2.findContours(images[-1],
                                                 cv2.RETR_LIST,
                                                 cv2.CHAIN_APPROX_SIMPLE) #CHAIN_APPROX_SIMPLE to simplify stored coordinates_only points
    #display contour and hierarchy info
    if control == ord("i"):
        print("Find Contour here:\n %s"%contours) #print on console
        print("Find Hierarchy here: \n %s"%hierarchy) #print on console
        
    #find contour with max area with the thresholds and store it as best_cnt
    #we assume the object with the largest area is the object we are looking for
    max_area=0
    best_cnt=1
    for cnt in contours:
        area=cv2.contourArea(cnt) #find area 
        if area> max_area:
            max_area= area
            best_cnt=cnt #contour with largest area
            
    #find centroid of best_cnt and draw circle
    M= cv2.moments(best_cnt)
    cx, cy=int (M['m10']/M['m00']), int (M['m01']/M['m00']) #find coordinates of the object's centroid
    
    #draw marker to indicate the centroid of the object 
    if max_area>0:
        #draw circle-shaped marker of high threshold color
        cv2.circle(raw_image, (cx, cy), 8, (THRESH_HI[threshold]), -1)
        #draw circle-shaped marker of low threshold color
        cv2.circle(raw_image, (cx, cy), 4, (THRESH_LOW[threshold]), -1)
        
    return(images, text, max_area)