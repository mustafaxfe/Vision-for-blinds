import time
import picamera

with picamera.PiCamera() as camera:
    #camera.resolution = (1296,972)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(10)
    camera.capture('im_source.jpg')
