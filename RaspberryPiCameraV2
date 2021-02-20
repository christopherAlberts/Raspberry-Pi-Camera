# importing the necessary modules
from datetime import datetime
from gpiozero import Button
import picamera
import time
import sys
import logging
import os
from subprocess import call

toggle_button = Button(21)  # Red wire (next to ground)
action_button = Button(20)  # Yellow wire
# webStreaming = Button(16)
killAndShutdown = Button(26) # Orange Wire

picam = picamera.PiCamera()
running = True
recording = False
streaming = False

# Location where files will be stored:
# Please ensure these folder exist before
# running this script
pictureLocation = '/home/pi/Camera/Picture/'
videoLocation = '/home/pi/Camera/Video/'
logFileLocation = '/home/pi/Camera/Log/'

# Setup logging so it logs to a file in logFileLocation:
fm = logFileLocation + 'log' + str(datetime.now()) + '.txt'
logging.basicConfig(filename=fm, filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# use this to set the resolution if you dislike the default values
picam.resolution = (960, 640)
# picam.brightness = 50 (0, 100)
# picam.sharpness = 0 (-100, 100)
# picam.contrast = 0 (-100, 100)
# picam.saturation = 0 (-100, 100)
# picam.iso = 0 (automatic) (100, 800)
# picam.exposure_compensation = 0 (-25, 25)
# picam.exposure_mode = 'auto'
# picam.meter_mode = 'average'
# picam.awb_mode = 'auto'
# picam.rotation = 0
# picam.hflip = False
# picam.vflip = False
# picam.crop = (0.0, 0.0, 1.0, 1.0)
# picam.shutter_speed = 6000000




def picture():
    timestamp = datetime.now()

    # Adding a text to live feed
    picam.annotate_text_size = 50
    picam.annotate_text = "Taking Photo!"
    time.sleep(1)
    picam.annotate_text = ""

    picam.resolution = (1920, 1080)
    picam.capture(pictureLocation + 'pic' + str(timestamp) + '.jpg')  # taking the picture
    picam.resolution = (960, 640)

    logging.info(str(timestamp) + ' - Taking photo')



def video_start():
    global recording
    recording = True
    timestamp = datetime.now()

    # Adding a text to live feed
    picam.annotate_text_size = 50
    picam.annotate_text = "Recording Video!"
    time.sleep(0.5)
    picam.annotate_text = ""

    picam.video_stabilization = True
    picam.start_recording(videoLocation + 'video' + str(timestamp) + '.h264')

    logging.info(str(timestamp) + ' - Video recording...')


def video_stop():
    global recording
    recording = False
    timestamp = datetime.now()

    picam.stop_recording()
    picam.video_stabilization = False

    # Adding a text to live feed
    picam.annotate_text_size = 50
    picam.annotate_text = "Stopping Recording!"
    time.sleep(1.5)
    picam.annotate_text = ""

    logging.info(str(timestamp) + ' - Video stopped ')



# def webstreaming_start():
#   global streaming
#   streaming = True
#   timestamp = datetime.now()
#   logging.info(str(timestamp) + ' - webstreaming start ')
#   os.system('raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24 |cvlc -vvv stream:///dev/stdin --sout \'#standard{access=http,mux=ts,dst=:8160}\' :demux=h264')

# def webstreaming_stop():
#   global streaming
#   streaming = False
#   timestamp = datetime.now()
#   logging.info(str(timestamp) + ' - webstreaming start ')
#   os.system('exit')

def kill_camera():
    timestamp = datetime.now()
    picam.stop_preview()
    logging.info(str(timestamp) + ' - End program due to kill_camera()')
    running = False

    # The following code will shutdown the Raspberry Pi
    # print('Shutting down Raspberry Pi...')
    # call("sudo shutdown -h now", shell=True)

    # The following code will terminate the program
    sys.exit()


picam.start_preview()  # running the preview

try:
    # MAIN LOOP
    while running:

        toggle_button_status = toggle_button.is_pressed
        if(toggle_button_status and action_button.is_pressed and recording == False):
            print('Taking picture ')
            picture()
            picam.annotate_text = ""

        elif(toggle_button_status == False and action_button.is_pressed and recording == False):
            print('video_start()')
            video_start()

        elif (action_button.is_pressed and recording == True):
            print('video_stop()')
            video_stop()
            picam.annotate_text = ""

        elif (killAndShutdown.is_pressed):

            kill_camera()

        else:
            timestamp = datetime.now()
            logging.info(str(timestamp) + ' - Error: No condition in MAIN LOOP being hit. ')

# we detect Ctrl+C then quit the program
except KeyboardInterrupt:
    timestamp = datetime.now()
    logging.warning(str(timestamp) + ' - End program due to KeyboardInterrupt')
    picam.stop_preview()
    running = False

