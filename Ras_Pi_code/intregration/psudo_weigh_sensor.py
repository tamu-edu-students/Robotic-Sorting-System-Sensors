import json


with open("Chap2\subsystem_connection.json", "r") as f:      # read the json file
  variables = json.load(f)

#see if i could read it
my_weight = variables["weight1"]  
#print(my_weight)
#print("it works")


#let say if their is a new reading from the weight sensor, since its a fruit went into a bin
d_output0 = 30

variables["weight1"] = d_output0   # change the variable in python

with open("C:/Users/lam12/OneDrive/Desktop/opencv/Chap2/subsystem_connection.json", "w") as f:      # write back to the json file
  json.dump(variables, f)

