from picamera.array import PiRGBArray
from picamera import PiCamera

import Adafruit_CharLCD as LCD
import http.client, urllib.parse
import RPi.GPIO as GPIO
import time
import cv2
import opencv_color_detect as PROCESS

totalrecyc=0
button=17
ledr=2
ledg=3
buzzer=21
#instantiate LCD and specify pins
lcd_rs=26
lcd_en=19
lcd_d4=13
lcd_d5=6
lcd_d6=5
lcd_d7=11
lcd_backlight=2

#define lcd size row and col
lcd_columns=16
lcd_rows=2
lcd=LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #we use BOARD ports reference
GPIO.setup(button,GPIO.IN, pull_up_down=GPIO.PUD_UP) #declare button  as an input
#pull_up_down=GPIO.PUD_UP means default state is true 
GPIO.setup(ledr,GPIO.OUT) #declare gpio 2 as an output
GPIO.setup(ledg,GPIO.OUT) #declare gpio 3 as an output
GPIO.setup(buzzer,GPIO.OUT, initial= GPIO.LOW) #declare gpio 27 as an output

def lcd_init():
    lcd.clear()
    lcd.cursor=(0,0)
    lcd.message('Welcome to EcoTruck')
    lcd.cursor=(1,0)
    lcd.message('Total recyc:')

def thingspeakRead(x):
    params=urllib.parse.urlencode({"field1":x,"key":"PY42TLQSA95U65MP"})
    headers= {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/plain"}                
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST","/update", params, headers)
        response= conn.getresponse()
        print(response.status, response.reason)
        data=response.read()
        connn.close()
    except:
        print("Connection Failed")

#show frame
def show_images(images,text,MODE):
    #add text to (image[MODE]) with respective MODE # and text
    cv2.putText(images[MODE], "%s:%s" %(MODE, text[MODE]), (10,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
    cv2.imshow("Frame", images[MODE]) #display frame
    
#INIT camera and take reference raw capture
def eco_truck():
    camera=PiCamera()
    camera.resolution=(640,480)
    camera.framerate=50 #frequency of frames capture of 50 frames per second 
    camera.hflip=True #flip image 
    
    rawCapture= PiRGBArray(camera, size=(640,480)) #convert to format for opencv processing 
    
    #warmup camera and init MODE
    time.sleep(0.1) #sleep 0.1s
    print("Starting camera...")
    MODE=0
    max_area=0
    
    #take frame from camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                #save pressed keys
        key=cv2.waitKey(1) & 0xFF
        
        #pass every new frame and key pressed to process_image()
        images, text, max_area= PROCESS.process_image(frame.array, key)
        
        #check key to change mode or quit
        if key == ord("m"):
            
            MODE=(MODE+1)%len(images)
        elif key == ord("q"): #if q is pressed means the user wants to exit
            print("Quit")
            break
        
        
        #display result images with text and respective mode
        show_images(images, text, MODE)
        
        
        #clear stream for the next frame
        rawCapture.truncate(0)
        
        #test and print area of wanted object
        print("TEST MAX AREA: %d"%max_area)
        
        #send http request to ThingSpeak
        thingspeakRead(max_area)
        
        ############################################
        #check key to change mode or quit
        if key == ord("m"):
            
            MODE=(MODE+1)%len(images)
        elif key == ord("q"): #if q is pressed means the user wants to exit
            print("Quit")
            break
        #####################################################
        
        if (max_area > 0): #wanted object detected
            print("Recyclable item detected! \n")
            totalrecyc+=1
            #LCD
            lcd.cursor=(1,13)
            lcd.message(totalrecyc)
            #LEDS
            GPIO.output(ledr,0) #turn off red LED
            GPIO.output(ledg,1) #turn on green LED
            time.sleep(5)
            GPIO.output(ledg,0)
            #Buzzer
            GPIO.output(buzzer,1) #turn on actibe buzzer for 3s
            time.sleep(2) 
            GPIO.output(buzzer,0) #turn off active buzzer
    
            
        elif (max_area == 0): #wanted object NOT detected
            print("NO recyclable item detected! \n")
            #LCD
            
            #LEDS
            GPIO.output(ledg,0) #turn off green LED
            GPIO.output(ledr,1) #turn on red LED
            time.sleep(5)
            GPIO.output(ledr,0)
            #Buzzer
            GPIO.output(buzzer,1) 
            time.sleep(0.5)
            GPIO.output(buzzer,0) 
            time.sleep(0.5)
            GPIO.output(buzzer,1)
            time.sleep(0.5)
            GPIO.output(buzzer,0)
            time.sleep(0.5)
            GPIO.output(buzzer,1)
            time.sleep(0.5)
            GPIO.output(buzzer,0)
            
            time.sleep(2)
            ############################################
            #check key to change mode or quit
            if key == ord("m"):
                
                MODE=(MODE+1)%len(images)
            elif key == ord("q"): #if q is pressed means the user wants to exit
                print("Quit")
                break
            #####################################################

       
print ('Welcome to EcoTruck SMART system!, thank you for choosing us.')
time.sleep(7)
def lcd_init()
while 1:
    #initialize LEDs
    GPIO.output(ledr,0) 
    GPIO.output(ledg,0)
    
    #check if button is pressed
    var =GPIO.input(button)
        #if flase, button is pressed
    if (var==False):
        print ('Button pressed, automated sorting activated')
            #call begin_capture function
        eco_truck()
        
    elif (var==True):
        print ('Button not pressed, please press to start')
        time.sleep(2)
        
GPIO.cleanup() #clear GPIO last outputs/states
    
        
         