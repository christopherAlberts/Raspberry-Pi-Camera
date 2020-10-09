# importing the necessary modules
from datetime import datetime
from gpiozero import Button
import picamera
import time
import sys
from subprocess import call

takePhoto = Button(21)
takeVideo = Button(20)
killAndShutdown = Button(26)

picam = picamera.PiCamera()
running = True
recording = False

# use this to set the resolution if you dislike the default values
picam.resolution = (1024, 768)

def picture():
    timestamp = datetime.now()
    picam.capture('/home/pi/Camera/Picture/pic' + str(timestamp) + '.jpg')  # taking the picture
    print('Taking photo')
    
def video_start():
    global recording
    recording = True
    timestamp = datetime.now()
    print('Video recording...')
    picam.start_recording('/home/pi/Camera/Video/video' + str(timestamp) + '.h264')
    time.sleep(1)
        
def video_stop():
    global recording
    recording = False
    print('Video stoped')
    picam.stop_recording()
    time.sleep(1)

def kill_camera():
    picam.stop_preview()
    print('End program due to kill_camera()')
    running = False
    
    # The following code will shutdown the Raspberry Pi
    #print('Shutting down Raspberry Pi...')
    #call("sudo shutdown -h now", shell=True)
    
    #The following code will terminate the program
    sys.exit()

picam.start_preview()  # running the preview

try:
    while running:
        #print('Active')  # displaying 'active' to the shell

        if (takePhoto.is_pressed):
            picture()
        elif (takeVideo.is_pressed and recording == False):
            video_start()
        elif (takeVideo.is_pressed and recording == True):
            video_stop()
        elif (killAndShutdown.is_pressed):
            kill_camera()
        
# we detect Ctrl+C then quit the program
except KeyboardInterrupt:
    print('End program due to KeyboardInterrupt')
    picam.stop_preview()
    running = False
    

