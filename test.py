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

dict = {'state': True}

while True:
    if (wm.state['buttons'] & cwiid.BTN_A):
        wm.close()
        print "WiiMote Closed"
        dict['state'] == False
        while dict['state'] = False:
            try:
                wm = cwiid.WiiMote()
                print "connecetion successful"
                wm.rumble = True
                time.sleep(.5)
                dict['state'] = True
                wm.rumble = False
            except:
                pass
    else:
        pass
