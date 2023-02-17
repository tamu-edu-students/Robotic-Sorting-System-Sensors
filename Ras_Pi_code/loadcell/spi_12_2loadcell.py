import spidev
import RPi.GPIO as GPIO
import time
import os

spi = spidev.SpiDev()
spi.open(0,0)

spi.max_speed_hz=1000000



#from the MCP3208 datasheet
#maybe no function
def readCh(channel):
    rec_data = spi.xfer2([6,0,0])
    d_output = ((rec_data[1]&15) << 8) + rec_data[2]
    return d_output

#from digtial to analog
def covDtoA(dig_val):
    volt = (dig_val*3.3)/4096
    return volt

#output pounds
# def convPounds(dig_val):


####### for the first load cell connected to channel 0
rec_data0 = spi.xfer2([6,0,0])
d_output0 = ((rec_data0[1]&15) << 8) + rec_data0[2]
####### for the first load cell connected to channel 1
rec_data1 = spi.xfer2([6,64,0])
d_output1 = ((rec_data1[1]&15) << 8) + rec_data1[2]

####### for the first load cell connected to channel 2
rec_data2 = spi.xfer2([6,128,0])
d_output2 = ((rec_data1[1]&15) << 8) + rec_data1[2]

while True:
    ####### for the first load cell connected to channel 0
    rec_data0 = spi.xfer2([6,0,0])
    d_output0 = ((rec_data0[1]&15) << 8) + rec_data0[2]
    load_cell1_volt = covDtoA(d_output0)
    ####### for the first load cell connected to channel 1
    rec_data1 = spi.xfer2([6,64,0])
    d_output1 = ((rec_data1[1]&15) << 8) + rec_data1[2]
    load_cell2_volt = covDtoA(d_output1)




    ######print output
    #load cell 1 and ch0
    print("load cell ADC output: ", d_output0 )
    print("load cell ADC volt: ", load_cell1_volt )
    #load cell 2 and ch1
    print("load cell ADC output: ", d_output1 )
    print("load cell ADC volt: ", load_cell2_volt )

    #pause 
    time.sleep(1)
