import spidev
import RPi.GPIO as GPIO
import time
import numpy as np

spi = spidev.SpiDev()

spi.open(0,0) #<---do I need this

spi.max_speed_hz=2000000

import json
with open("subsystem_connection.json", "r") as f:      # read the json file
 variables = json.load(f)
 
 #from digtial to analog
def covDtoA(dig_val):
    volt = (dig_val*3.3)/4096
    return volt

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


### while loop with 12 inetation
i = 0 
while i < 13:
    rec_data0 = spi.xfer2([6,0,0])
    d_output0 = ((rec_data0[1]&15) << 8) + rec_data0[2]
    load_cell1_volt = covDtoA(d_output0)
    datalist1 = adddata(datalist1, d_output0)
    
    rec_data1 = spi.xfer2([6,64,0])
    d_output1 = ((rec_data1[1]&15) << 8) + rec_data1[2]
    load_cell2_volt = covDtoA(d_output1)
    datalist2 = adddata(datalist2, d_output1)
    
    rec_data2 = spi.xfer2([6,128,0])
    d_output2 = ((rec_data2[1]&15) << 8) + rec_data2[2]
    load_cell3_volt = covDtoA(d_output2)
    datalist3 = adddata(datalist3, d_output2)
    #print(i)
    i = i + 1
    
avg_list1 = np.mean(datalist1)
avg_list2 = np.mean(datalist2)
avg_list3 = np.mean(datalist3)

print(avg_list1)
#print(datalist1)
print(avg_list2)
#print(datalist2)
print(avg_list3)
#print(datalist3)

variables["weight1"] = avg_list1
variables["weight2"] = avg_list2
variables["weight3"] = avg_list3
with open("subsystem_connection.json", "w") as f:      # write back to the json file
    json.dump(variables, f)
    
#print("done")