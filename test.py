import cwiid
import time

dict = {'state' : True, 'wm' : []}

print "press 1 + 2 now"
try:
    # attempt to connect wii remote
    wm = cwiid.Wiimote()
except RuntimeError:
    print "failed to find wiimote"
print "wiimote found"
# set buttons to report when pressed
wm.rpt_mode = cwiid.RPT_BTN


wm.led = 15
time.sleep(3)
print dir(cwiid)
