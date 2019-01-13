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
#     time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
     lat = lat_long_decode(sdata[2])
     lat_dir = sdata[3]
     long = lat_long_decode(sdata[4])
     long_dir = sdata[5]
     alt = sdata[9]

     return  " " +  lat + " " + lat_dir + " " + long + " " + long_dir + " " + alt + " M"

######## end of parse gga  ##############


def parse_rmc(sdata):
     date = sdata[9]
     #date = data[9][0:2] + "-" + sdata[9][2:4] + "-" + sdata[9][4:6]
     time = sdata[1][0:6]
     #time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]

     print date + "_" + time
     return date + "_" + time
####### end of parse rmc  ##############




print "Looking for GPS Data"

while True:
   data = ser.read_until() 
# Uncomment following line for quick GPS test
#   print data 
   sdata = data.split(",")

   if sdata[0] == "$GPGGA":
           gps_fix  = parse_gga(sdata)
 
   if sdata[0] == "$GPRMC":

          timestamp = parse_rmc(sdata)
          break 





gps_string = timestamp + " " + gps_fix
print gps_string

ser.close()


#img = Image.new('RGB', (764, 1024), color = (73, 109, 137))
#img = Image.new('RGBA', (764, 1024), (255, 0, 0, 0))
img = Image.new('RGB', (1944, 60), color=(255,255,255))

print "gps_string"
print gps_string
#data = "Test 12"
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",40)
d = ImageDraw.Draw(img)
d.text((30,10), gps_string, font=font, fill=(0,0,0))
img.rotate(90,expand = True).save('foreground.jpg', 'JPEG')


#os.system('raspistill -v -gps -o cam.jpg > cam.out')
subprocess.Popen(['raspistill', '-v',  '-o', 'cam.jpg'])



background = Image.open("cam.jpg").convert("RGB")
foreground = Image.open("foreground.jpg")

background.paste(foreground, (0, 0)) #, foreground)
newname = "/home/pi/gonet/" + socket.gethostname()[-3:] + "_" + timestamp +".jpg"
print newname

background.save('composite.jpg', 'JPEG')
#background.save(filename, 'JPEG')
#background.save(socket.gethostname()[-3:] + "_" + timestamp + ".jpg", 'JPEG')



#subprocess.call(["mv", "composite.jpg", _filename])

os.rename('/home/pi/gonet/composite.jpg', newname)


