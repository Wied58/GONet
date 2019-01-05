#!/usr/bin/python

import serial
 
port = "/dev/serial0"

ser = serial.Serial(port, baudrate = 57600, timeout = 0.5)

#def lat_long_decode(coord):
#    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
#    x = coord.split(".")
#    head = x[0]
#    tail = x[1]
#    deg = head[0:-2]
#    min = head[-2:]cd gp
#    return deg + " deg " + min + "." + tail + " min"
######## end of lat_long_decode ##############


def parse_gga(sdata):
     alt = sdata[7]
     return alt
######## end of parse gga  ##############

print "Looking for GPS data"


count = 1

while True:
   data = ser.read_until() 
   sdata = data.split(",")

   if sdata[0] == "$GPGGA":
       alt = parse_gga(sdata)


   if sdata[0] == "$GPRMC":
       if sdata[2] == 'V':
          print "no satellite data available"
          date = sdata[9]
          time = sdata[1]
          lat = sdata[3]
          lat_dir = sdata[4]
          long = sdata[5]
          long_dir = sdata[6]
          print count
          count = count + 1
          print alt


