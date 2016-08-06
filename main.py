import cwiid
import time
from phue import Bridge

#Check config for defined rooms and the associated lights
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

wm.led = 1

dict = {'start' : 0, 'end' : 0, 'room1' : [], 'room2' : [], 'bright' : 0, 'group_state' : True, 'room_name': '', 'timer' : 0, 'repeat_cycle' : True}

#START DEFINING ROOMS
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

b.create_group('room1', dict['room1'])
b.create_group('room2', dict['room2'])
#END DEFINING ROOMS

def rumble(wm):
    wm.rumble = True
    time.sleep(.1)
    wm.rumble = False

def change_lights(wm):
    try:
        light_number = wm.state['led']
        led_state = b.get_light(light_number, 'on')
        if led_state == True:
            b.set_light(light_number, 'on', False)
            dict['bright'] = 0
        elif led_state == False:
            b.set_light(light_number, 'on', True)
            dict['bright'] = 254
    except TypeError:
        print 'no attached light'
        rumble(wm)
        rumble(wm)

def led_increase(wm):
    led_state = wm.state['led']
    if led_state >= 16:
        wm.led = 0
    else:
        wm.led = led_state + 1

def check_leds(wm):
    if wm.state['led'] >= 16:
        wm.led = 15
    if wm.state['led'] <= 1:
        wm.led = 1

def checkset_bright(wm):
    if dict['bright'] >= 250:
        dict['bright'] = 254
    if dict['bright'] <= 25:
        dict['bright'] = 0
    light_number = wm.state['led']
    b.set_light(light_number, 'bri', dict['bright'])

def change_group_light():
    light_set = dict[dict['room_name']]
    #light_set = dict[indict]
    if dict['group_state'] == True:
        b.set_light(light_set, 'on', False)
        dict['group_state'] = False
    elif dict['group_state'] == False:
        b.set_light(light_set, 'on', True)
        dict['group_state'] = True

def read_btns(wm):
    if (wm.state['buttons'] & cwiid.BTN_UP):
        wm.led = wm.state['led'] + 1
        rumble(wm)
        check_leds(wm)
        reset_timer()

    #DOWN
    if (wm.state['buttons'] & cwiid.BTN_DOWN):
        wm.led = wm.state['led'] - 1
        rumble(wm)
        check_leds(wm)
        reset_timer()

    #A
    if (wm.state['buttons'] & cwiid.BTN_A):
        change_lights(wm)
        rumble(wm)
        reset_timer()

    #LEFT
    if (wm.state['buttons'] & cwiid.BTN_LEFT):
        dict['bright'] = dict['bright'] - 50
        checkset_bright(wm)
        rumble(wm)
        reset_timer()

    #RIGHT
    if (wm.state['buttons'] & cwiid.BTN_RIGHT):
        dict['bright'] = dict['bright'] + 50
        checkset_bright(wm)
        rumble(wm)
        reset_timer()

    #ONE
    if (wm.state['buttons'] & cwiid.BTN_1):
        dict['room_name'] = 'room1'
        change_group_light()
        rumble(wm)
        reset_timer()

    #TWO
    if (wm.state['buttons'] & cwiid.BTN_2):
        dict['room_name'] = 'room2'
        change_group_light()
        rumble(wm)
        reset_timer()

    else:
        time_to_reset = dict['timer']
        dict['timer'] = time_to_reset + 1
        if dict['timer'] == 10:
            wm.close()
            mote_not_connected(wm)

while True:
    if dict['repeat_cycle'] == True:
        read_btns(wm)
        dict['timer'] += 1
        if dict['timer'] <= 10:
            dict['timer'] = 0
            wm.close()
            print "remote disconnected"
            dict['repeat_cycle'] = False
    if dict['repeat_cycle'] == False:
        print 'looking for remote'
        try:
            # attempt to connect wii remote
            wm = cwiid.Wiimote()
        except RuntimeError:
            print "failed to find wiimote"
        print "wiimote found"
        # set buttons to report when pressed
        wm.rpt_mode = cwiid.RPT_BTN

        time.sleep(.1)
