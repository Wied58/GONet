#!/usr/bin/python

import serial
 
most_of_gps = ""
alt = ""

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
     alt = sdata[9]
     return alt
######## end of parse gga  ##############


def parse_rmc(sdata):
     date =data[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]
     time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
     lat = sdata[3]
     lat_dir = sdata[4]
     long = sdata[5]
     long_dir = sdata[6]
     
     return date + " " + time + " " +  lat + " " + lat_dir + " " + long + " " + long_dir
     #print  date + " " + time + " " +  lat + " " + lat_dir + " " + long + " " + long_dir
####### end of parse rmc  ##############




print "Looking for GPS Data"

while True:
   data = ser.read_until() 
#   print data
   sdata = data.split(",")

   if sdata[0] == "$GPGGA":
       alt = parse_gga(sdata)

   if sdata[0] == "$GPRMC":
#       if sdata[2] == 'V':
#          print "no satellite data available"
# this would be a great place for an else           

          most_of_gps = parse_rmc(sdata)
          break 





gps_string =  most_of_gps + " " + alt
print gps_string


