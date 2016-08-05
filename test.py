import cwiid
import time

wm.led = 15

dict = {'state' : False}

while True:

    if dict['state'] == True:
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
