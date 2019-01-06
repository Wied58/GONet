#!/usr/bin/python

import serial
 
most_of_gps = ""
date = ""

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
     time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
     lat = lat_long_decode(sdata[2])
     lat_dir = sdata[3]
     long = lat_long_decode(sdata[4])
     long_dir = sdata[5]
     alt = sdata[9]

     return time + " " +  lat + " " + lat_dir + " " + long + " " + long_dir + " " + alt + " M"

######## end of parse gga  ##############


def parse_rmc(sdata):
     date =data[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]
 
     return date
####### end of parse rmc  ##############




print "Looking for GPS Data"

while True:
   data = ser.read_until() 
#   print data
   sdata = data.split(",")

   if sdata[0] == "$GPGGA":
       most_of_gps  = parse_gga(sdata)

   if sdata[0] == "$GPRMC":
#       if sdata[2] == 'V':
#          print "no satellite data available"
# this would be a great place for an else           

          date = parse_rmc(sdata)
          break 





gps_string = date + " " + most_of_gps
print gps_string


