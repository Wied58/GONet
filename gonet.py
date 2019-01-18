#!/usr/bin/python

import serial
import subprocess
import socket
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
 
gps_fix = ""
timestamp = ""



port = "/dev/serial0"
ser = serial.Serial(port, baudrate = 57600, timeout = 0.5)

def lat_long_decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]

    return deg + " deg " + min + "." + tail + " min"

######## end of lat_long_decode ##############


def parse_gga(sdata):
     lat = lat_long_decode(sdata[2])
     lat_dir = sdata[3]
     long = lat_long_decode(sdata[4])
     long_dir = sdata[5]
     alt = sdata[9]

     return  " " +  lat + " " + lat_dir + " " + long + " " + long_dir + " " + alt + " M"

######## end of parse gga  ##############


def parse_rmc(sdata):
     date = sdata[9]
     time = sdata[1][0:6]

     print date + "_" + time
     return date + " " + time
####### end of parse rmc  ##############

def convert_raw_timestamp_to_filename_timestamp(raw_timestamp):
     time_parts = raw_timestamp.split(" ")
     return time_parts[0] + "_" + time_parts[1]
######### convert_raw_to_filename ##################


def  convert_raw_timestamp_to_image_timestamp(raw_timestamp):
     #180119_214946 DD/MM/YY HH:MM:SS
     date = raw_timestamp[0:2] + "/" + raw_timestamp[2:4] + "/" + raw_timestamp[4:6]
     time = raw_timestamp[7:9] + ":" + raw_timestamp[9:11] + ":" + raw_timestamp[11:13]
     return date + " " + time
############### end of convert_raw_timestamp_to_filename_timestamp ########################
print  "Looking for GPS Data"

while True:
   data = ser.read_until() 
# Uncomment following line for quick GPS test
#   print data 
   sdata = data.split(",")

   if sdata[0] == "$GPGGA":
           raw_gps_fix  = parse_gga(sdata)
 
   if sdata[0] == "$GPRMC":

          raw_timestamp = parse_rmc(sdata)
          break 

ser.close()

filename_timestamp = convert_raw_timestamp_to_filename_timestamp(raw_timestamp)

image_timestamp = convert_raw_timestamp_to_image_timestamp(raw_timestamp)
print image_timestamp

#image_gps_fix = convert_raw_gps_fix_to_image_gps_fix(raw_gps_fix)

gps_string = raw_timestamp + " " + raw_gps_fix

#ser.close()


#img = Image.new('RGB', (764, 1024), color = (73, 109, 137))
#img = Image.new('RGBA', (764, 1024), (255, 0, 0, 0))
img = Image.new('RGB', (1944, 120), color=(255,255,255))

print "gps_string"
print gps_string
#data = "Test 12"
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",40)
d = ImageDraw.Draw(img)
d.text((20,10), "Adler / Far Horizons GONet hostname: " + socket.gethostname(), font=font, fill=(0,0,0))
d.text((20,70), gps_string, font=font, fill=(0,0,0))
img.rotate(90,expand = True).save('foreground.jpg', 'JPEG')

subprocess.Popen(['raspistill', '-v',  '-o', 'cam.jpg'])

background = Image.open("cam.jpg").convert("RGB")
foreground = Image.open("foreground.jpg")

background.paste(foreground, (0, 0)) #, foreground)

background.save(socket.gethostname()[-3:] + "_" + filename_timestamp + ".jpg", 'JPEG')

