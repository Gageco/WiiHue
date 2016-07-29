import time
from phue import Bridge


f = open("./config.py")
lines = f.readlines()
f.close()
bridge_ip = eval(lines[1])
b = Bridge(bridge_ip)

dict = {'start' : 0, 'end' : 0, 'room1' : [], 'room2' : []}


x = [1,2]
b.set_light(x, 'on', True)
