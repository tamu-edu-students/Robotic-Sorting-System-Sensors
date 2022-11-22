import spidev
import RPi.GPIO as GPIO
import time
import os

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 0b00
spi.max_speed_hz=1000000



#from the MCP3008 datasheet
def readCh(channel):
    rec_data = spi.xfer2([1,(8+channel)<<4,0])
    d_output = ((rec_data[1]&3) << 8) + rec_data[2]
    return d_output

#from digtial to analog
def covDtoA(dig_val):
    volt = (dig_val*3.3)/1023
    return volt

#output pounds
# def convPounds(dig_val):

ch0 = 0

while True:
    #read output from the load cell
    load_cell_val = readCh(ch0)



    #print output
    print("load cell ADC output: ", load_cell_val )

    #pause 
    time.sleep(1)