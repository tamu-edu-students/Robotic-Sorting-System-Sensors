import json

###to test the json file to see if it could update current weight value

with open("Chap2\subsystem_connection.json", "r") as f:      # read the json file
  variables = json.load(f)
  

#note depending what sorting setting is in place, the var "fruit" can be hue, heigh, width, or goood (1) to bad (0)

#see if i could read it in the context of the ML model
GoodOrBad = variables["fruit"]  
print(GoodOrBad)
print("^- reading from the intial json file")

#let say that the next fruit that the ML detect it as bad
nextFruit = 0

variables["fruit"] = nextFruit   # change the variable in python

with open("C:/Users/lam12/OneDrive/Desktop/opencv/Chap2/subsystem_connection.json", "w") as f:      # write back to the json file
  json.dump(variables, f)

GoodOrBad = variables["fruit"]  
print(GoodOrBad)
print("^- reading from the json file with the bad quality fruit")

#let say that the next fruit that the ML detect it as good
nextFruit = 1
variables["fruit"] = nextFruit   # change the variable in python
with open("C:/Users/lam12/OneDrive/Desktop/opencv/Chap2/subsystem_connection.json", "w") as f:      # write back to the json file
  json.dump(variables, f)
  GoodOrBad = variables["fruit"]  
print(GoodOrBad)
print("^- reading from the json file with the good quality fruit")
