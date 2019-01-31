#!/usr/bin/python

import piexif
import serial
import subprocess
import socket
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ExifTags
 
gps_fix = ""
timestamp = ""



port = "/dev/serial0"
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

def lat_long_decode(coord):
    #Converts DDDMM.MMMMM > DD  MM' SS.SSS" 
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    sec = str((float(tail)/1000) * 60.0)

    #return deg + "  " + min + " " + sec + " "
    return deg + " DEG " + min + " \"" + sec + " \""

######## end of lat_long_decode ##############


def parse_gga(sdata):
     lat = sdata[2]
     lat_dir = sdata[3]
     long = sdata[4]
     long_dir = sdata[5]
     alt = sdata[9]

     return  lat + " " + lat_dir + " " + long + " " + long_dir + " " + alt + " M"

######## end of parse gga  ##############


def parse_rmc(sdata):
     date = sdata[9]
     time = sdata[1][0:6]
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


def convert_raw_gps_fix_to_image_gps_fix(raw_gps_fix):
     #4203.4338 N 08748.7831 W 215.3 M
     lat = lat_long_decode(raw_gps_fix[0:8])
     lat_dir = raw_gps_fix[10]
     long = lat_long_decode(raw_gps_fix[12:21])
     long_dir = raw_gps_fix[23]
     alt = raw_gps_fix[25:30]

     return  lat + " " + lat_dir + " " + long + " " + long_dir + " " + alt + " M"

######### end of convert_raw_gps_fix_to_image_gps_fix  ##############

def convert_raw_gps_fix_to_exif_lat(raw_gps_fix):
     raw_lat = (raw_gps_fix.split(" "))[0]
     deg = raw_lat[0:2]
     min = raw_lat[2:4]
     sec = str(int((float(raw_lat[4:9]) * 60.0)))
     return deg + "/1," + min + "/1," + sec + "/1"

def convert_raw_gps_fix_to_exif_long(raw_gps_fix):
     raw_lat = (raw_gps_fix.split(" "))[2]
     deg = raw_lat[0:3]
     min = raw_lat[3:5]
     sec = str(int((float(raw_lat[5:10]) * 60.0)))
     return deg + "/1," + min + "/1," + sec + "/1"

#############################################
######### Start of main program #############
#############################################


print  "Looking for GPS Data"

while True:
   data = ser.read_until() 
# Uncomment following line for quick GPS test
#   print data 
   sdata = data.split(",")

   if sdata[0] == "$GPRMC":
          raw_timestamp = parse_rmc(sdata)

   if sdata[0] == "$GPGGA":
          raw_gps_fix  = parse_gga(sdata)
          break 

ser.close()

######## done with gps ##############

######## manuipilate gps strings to make them useful ###########

filename_timestamp = convert_raw_timestamp_to_filename_timestamp(raw_timestamp)

image_timestamp = convert_raw_timestamp_to_image_timestamp(raw_timestamp)
print image_timestamp

image_gps_fix = convert_raw_gps_fix_to_image_gps_fix(raw_gps_fix)
print image_gps_fix

gps_string = raw_timestamp + " " + raw_gps_fix

exif_lat = convert_raw_gps_fix_to_exif_lat(raw_gps_fix)
exif_long = convert_raw_gps_fix_to_exif_long(raw_gps_fix)



######### done with gps string manipu
#Create image of a white rectangle for test background
img = Image.new('RGB', (1944, 120), color=(255,255,255))

print "gps_string "
print gps_string

# place black text on white image, rotate and save as foreground.jpg
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",40)
d = ImageDraw.Draw(img)
d.text((20,10), "Adler / Far Horizons GONet hostname: " + socket.gethostname(), font=font, fill=(0,0,0))
d.text((20,70), image_timestamp + " " + image_gps_fix, font=font, fill=(0,0,0))
img.rotate(90,expand = True).save('foreground.jpg', 'JPEG')

# take a picture with pi cam!
#subprocess.Popen(['raspistill', '-v',  '-o', 'cam.jpg'])


#exif_lat = '42/1,03/1,25.86/1'
#exif_long = '087/1,48/1,46.9794/1'

# http://www.ridgesolutions.ie/index.php/2015/03/05/geotag-exif-gps-latitude-field-format/
#https://sno.phy.queensu.ca/~phil/exiftool/TagNames/GPS.html


#subprocess.Popen(['raspistill', '-v', 
#                                '-x', 'GPS.GPSLatitude=42/1,3/10,43/100',
#                                '-x', 'GPS.GPSLongitude=87/1,48/10,78/100', 
#                                '-o', 'cam.jpg'], shell=True)

#08748.77952
command = ['raspistill', '-v',
                         '-x', 'GPS.GPSLatitude=' + exif_lat,
                         '-x', 'GPS.GPSLatitudeRef=' + "N",
                         '-x', 'GPS.GPSLongitude=' + exif_long, 
                         '-x', 'GPS.GPSLongitudeRef=' + "W",
                         '-o', 'cam.jpg']
subprocess.Popen(command)

# open the the image from pi cam 
background = Image.open("cam.jpg").convert("RGB")

# save its exif
exif = background.info['exif']


# open foreground.jpg and paste it to pi cam image
foreground = Image.open("foreground.jpg")
background.paste(foreground, (0, 0)) #, foreground)

#save the new composite image with pi cam photo's exif
background.save(socket.gethostname()[-3:] + "_" + filename_timestamp + ".jpg", 'JPEG',  exif=exif)
#background.save(socket.gethostname()[-3:] + "_" + filename_timestamp + ".jpg", 'JPEG')

