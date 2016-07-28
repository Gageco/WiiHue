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

#Check config for defined rooms and the associated lights
f = open("./config.py")
lines = f.readlines()
f.close()

dict = {'start' : 0, 'end' : 0, 'room1' : [], 'room2' : []}

linenum = 0
for txt_line in lines:
    try:
        txt = eval(lines[linenum])
        if txt == 'START':
            dict['start'] = linenum
        if txt =='END':
            dict['end'] = linenum
    except SyntaxError:
        pass
    linenum += 1
eval_line_txt = dict['start']

room_num = 0
while eval_line_txt != dict['end'] - 1:
    eval_line_txt += 1
    evaled_lines = eval(lines[eval_line_txt])
    room_num += 1
    room_num_txt = 'room' + str(room_num)
    dict[room_num_txt] = evaled_lines[1]
    print dict[room_num_txt]

b.create_group('room1', str(dict['room1']))
b.create_group('room2', str(dict['room2']))

def rumble():
    wm.rumble = True
    time.sleep(.1)
    wm.rumble = False

def change_lights():
    light_number = wm.state['led']
    led_state = b.get_light(light_number, 'on')
    if led_state == True:
        b.set_light(light_number, 'on', False)
        dict['bright'] = 0
    if led_state == False:
        b.set_light(light_number, 'on', True)
        dict['bright'] = 254

def led_increase():
    led_state = wm.state['led']
    if led_state >= 16:
        wm.led = 0
    else:
        wm.led = led_state + 1

def check_leds():
    if wm.state['led'] >= 16:
        wm.led = 15
    if wm.state['led'] <= 0:
        wm.led = 0

def checkset_bright():
    if dict['bright'] >= 250:
        dict['bright'] = 254
    if dict['bright'] <= 4:
        dict['bright'] = 0
    light_number = wm.state['led']
    b.set_light(light_number, 'bri', dict['bright'])

def change_group_light(room_name):
    led_state = b.get_light(room_name, 'on')
    if led_state == True:
        b.set_light(room_name, 'on', False)
    if led_state == False:
        b.set_light(room_name, 'on', True)

dict = {'bright' : 0}

while True:

    if (wm.state['buttons'] & cwiid.BTN_UP):
        wm.led = wm.state['led'] + 1
        rumble()
        check_leds()

    if (wm.state['buttons'] & cwiid.BTN_DOWN):
        wm.led = wm.state['led'] - 1
        rumble()
        check_leds()

    if (wm.state['buttons'] & cwiid.BTN_A):
        change_lights()
        rumble()

    if (wm.state['buttons'] & cwiid.BTN_LEFT):
        dict['bright'] = dict['bright'] - 50
        checkset_bright()
        rumble()

    if (wm.state['buttons'] & cwiid.BTN_RIGHT):
        dict['bright'] = dict['bright'] + 50
        checkset_bright()
        rumble()

    if (wm.state['buttons'] & cwiid.BTN_1):
        room_name = 'room1'
        change_group_light(room_name)
        rumble()

    if (wm.state['buttons'] & cwiid.BTN_2):
        room_name = 'room2'
        change_group_light(room_name)
        rumble()

    time.sleep(.3)
