#!/usr/bin/python

import serial
 
port = "/dev/serial0"

ser = serial.Serial(port, baudrate = 57600, timeout = 0.5)

print "Receiving GPS data"


count = 1

while True:
   data = ser.read_until() 
   sdata = data.split(",")

   if sdata[0] == "$GPRMC":
       if sdata[2] == 'V':
          print "no satellite data available"
          date = sdata[9]
          time = sdata[1]
          lat = sdata[3]
          lat_dir = sdata[4]
          long = sdata[5]
          long_dir = sdata[6]
   if sdata[0] == "$GPGGA"
          alt = sdata[7]


          print count
          count = count + 1
          print data



