import cwiid
import time

print "press 1 + 2 now"
try:
    # attempt to connect wii remote
    wm = cwiid.Wiimote()
except RuntimeError:
    print "failed to find wiimote"
print "wiimote found"

wm.led = 0

while True:
    wm.led = wm.state['led'] + 1
    time.sleep(3600)
    wm.led = wm.state['led'] + 1
