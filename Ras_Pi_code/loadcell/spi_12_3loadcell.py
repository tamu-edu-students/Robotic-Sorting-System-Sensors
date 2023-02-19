import spidev
import RPi.GPIO as GPIO
import time
import os
import numpy as np

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
####### for the second load cell connected to channel 1
rec_data1 = spi.xfer2([6,64,0])
d_output1 = ((rec_data1[1]&15) << 8) + rec_data1[2]

####### for the third load cell connected to channel 2
rec_data2 = spi.xfer2([6,128,0])
d_output2 = ((rec_data2[1]&15) << 8) + rec_data2[2]


datalist1 =[0,0,0,0,0,0,0,0,0,0,0,0]
datalist2 =[0,0,0,0,0,0,0,0,0,0,0,0]
datalist3 =[0,0,0,0,0,0,0,0,0,0,0,0]

def adddata(datalist, input):
    i = len(datalist)-2
    while i >= 0:
        datalist[i+1] = datalist[i]
        i = i-1
    datalist[0] = input
    return datalist


while True:
    ####### for the first load cell connected to channel 0
    rec_data0 = spi.xfer2([6,0,0])
    d_output0 = ((rec_data0[1]&15) << 8) + rec_data0[2]
    load_cell1_volt = covDtoA(d_output0)
    ####### for the first load cell connected to channel 1
    rec_data1 = spi.xfer2([6,64,0])
    d_output1 = ((rec_data1[1]&15) << 8) + rec_data1[2]
    load_cell2_volt = covDtoA(d_output1)
    ####### for the third load cell connected to channel 2
    rec_data2 = spi.xfer2([6,128,0])
    d_output2 = ((rec_data2[1]&15) << 8) + rec_data2[2]
    load_cell3_volt = covDtoA(d_output2)
    
    
    ######taking the mean for load cell 1
    datalist1 = adddata(datalist1, d_output0)
    avg_list1 = np.mean(datalist1)
    ######taking the mean for load cell 2
    datalist2 = adddata(datalist2, d_output1)
    avg_list2 = np.mean(datalist2)
    ######taking the mean for load cell 3
    datalist3 = adddata(datalist3, d_output2)
    avg_list3 = np.mean(datalist3)
    




    ######print output
    #load cell 1 and ch0
    print("For load cell 1")
    #print("load cell 1 ADC output: ", d_output0 )
    print("load cell 1 ADC volt: ", load_cell1_volt, "V" )
    print("list of prev 12 data: ", datalist1)
    print("the mean of the list: ", avg_list1)
    #load cell 2 and ch1
    print("For load cell 2")
    #print("load cell 2 ADC output: ", d_output1 )
    print("load cell 2 ADC volt: ", load_cell2_volt, "V")
    print("list of prev 12 data: ", datalist2)
    print("the mean of the list: ", avg_list2)
    #load cell 2 and ch2
    print("For load cell 3")
    #print("load cell 3 ADC output: ", d_output2 )
    print("load cell 3 ADC volt: ", load_cell3_volt, "V")
    print("list of prev 12 data: ", datalist3)
    print("the mean of the list: ", avg_list3)

    #pause 
    time.sleep(1)