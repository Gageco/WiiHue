import cwiid
import time

print "press 1 + 2 now"
try:
    # attempt to connect wii remote
    wm = cwiid.Wiimote()
except RuntimeError:
    print "failed to find wiimote"
print "wiimote found"

wm.led = 15

dict = {'state' : True}

while True:

    if dict['state'] == True
        while dict['state'] == True:
            if (wm.state['buttons'] & cwiid.BTN_A):
                wm.close()
                print "WiiMote Closed"
                dict['state'] = False


    if dict['state'] == False:
        while dict['state'] == False:
            print "1 + 2 now"
            wm = cwiid.WiiMote()
            print "connecetion successful"
            wm.rumble = True
            time.sleep(.5)
            dict['state'] = True
            wm.rumble = False

    time.sleep(.5)
