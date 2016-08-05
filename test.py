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

wm.close()
print "connection closed"

wm = cwiid.Wiimote()
print "connection found"
wm.led = 15
time.sleep(1)


wm.close()
print "connection closed"

wm = cwiid.Wiimote()
print "connection found"
