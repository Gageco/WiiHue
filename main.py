import cwiid
import time
from phue import Bridge

f = open("./config.py")
lines = f.readlines()
f.close()
bridge_ip = eval(lines[1])
b = Bridge(bridge_ip)
print "press 1 + 2 now"
try:
    # attempt to connect wii remote
    wm = cwiid.Wiimote()
except RuntimeError:
    print "failed to find wiimote"
print "wiimote found"
# set buttons to report when pressed
wm.rpt_mode = cwiid.RPT_BTN

while True:
    def rumble_when_pressed():
        wm.rumble = True
        time.sleep(.1)
        wm.rumble = False

    def change_lights():
        light_number = wm.state['led']
        led_state = b.get_light(light_number, 'on')
        if led_state == True:
            b.set_light(light_number, 'on', True)
        if led_state == False:
            b.set_light(light_number, 'on', False)
        rumble_when_pressed()

    def led_increase():
        led_state = wm.state['led']
        if led_state >= 16:
            wm.led = 0
        else:
            wm.led = led_state + 1

    if (wm.state['buttons'] & cwiid.BTN_UP):
        light_on()
    if (wm.state['buttons'] & cwiid.BTN_DOWN):
        light_off()
    if (wm.state['buttons'] & cwiid.BTN_A):
        change_lights()

    time.sleep(.3)