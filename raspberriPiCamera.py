# importing the necessary modules
from datetime import datetime
from gpiozero import Button
import picamera
import time
import sys
import logging
from subprocess import call

takePhoto = Button(21)
takeVideo = Button(20)
killAndShutdown = Button(26)

picam = picamera.PiCamera()
running = True
recording = False

# Location where files will be stored:
# Please ensure these folderd exsist before
# running this script
pictureLocation = '/home/pi/Camera/Picture/'
videoLocation = '/home/pi/Camera/Video/'
logFileLocation = '/home/pi/Camera/Log/'

# Setup logging so it logs to a file in logFileLocation:
fm = logFileLocation + 'log' + str(datetime.now()) + '.txt'
logging.basicConfig(filename=fm, filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# use this to set the resolution if you dislike the default values
# picam.resolution = (1024, 768)
picam.resolution = (500, 500)

def picture():
    timestamp = datetime.now()
    picam.capture(pictureLocation + 'pic' + str(timestamp) + '.jpg')  # taking the picture
    logging.info(str(timestamp) + ' - Taking photo')
    
def video_start():
    global recording
    recording = True
    timestamp = datetime.now()
    picam.start_recording(videoLocation + 'video' + str(timestamp) + '.h264')
    logging.info(str(timestamp) + ' - Video recording...')
    time.sleep(1)
        
def video_stop():
    global recording
    recording = False
    picam.stop_recording()
    timestamp = datetime.now()
    logging.info(str(timestamp) + ' - Video stoped ')
    time.sleep(1)

def kill_camera():
    timestamp = datetime.now()
    picam.stop_preview()
    logging.info(str(timestamp) + ' - End program due to kill_camera()')
    running = False
    
    # The following code will shutdown the Raspberry Pi
    #print('Shutting down Raspberry Pi...')
    #call("sudo shutdown -h now", shell=True)
    
    #The following code will terminate the program
    sys.exit()

picam.start_preview()  # running the preview

try:
    while running:

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
    timestamp = datetime.now()
    logging.warning(str(timestamp) + ' - End program due to KeyboardInterrupt')
    picam.stop_preview()
    running = False
    


    

    

