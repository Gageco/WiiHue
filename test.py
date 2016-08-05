import cwiid
import time

dict = {'state' : True, 'wm' : ''}

def connect_mote():
    print "press 1 + 2 now"
    try:
        # attempt to connect wii remote
        dict['wm'] = cwiid.Wiimote()
    except RuntimeError:
        print "failed to find wiimote"
    print "wiimote found"
    dict['wm'].rpt_mode = cwiid.RPT_BTN

x = dict['wm']
x.led = 15
