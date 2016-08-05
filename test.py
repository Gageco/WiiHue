import cwiid
import time

dict = {'state' : True, 'wm' : ''}

def connect_mote():
    print "press 1 + 2 now"
    try:
        # attempt to connect wii remote
        wm = cwiid.Wiimote()
        print type(wm)
    except RuntimeError:
        print "failed to find wiimote"
    print "wiimote found"
    wm.rpt_mode = cwiid.RPT_BTN

connect_mote()
wm.led = 15

while True:

    if dict['state'] == True:
        while dict['state'] == True:
            if (wm.state['buttons'] & cwiid.BTN_A):
                wm.close()
                print "WiiMote Closed"
                dict['state'] = False


    if dict['state'] == False:
        while dict['state'] == False:
            connect_mote()
            wm.rumble = True
            time.sleep(.5)
            dict['state'] = True
            wm.rumble = False

    time.sleep(.5)
