import cwiid
import time
from phue import Bridge
import requests

#Check config for later use
f = open("./config.py")
lines = f.readlines()
f.close()
bridge_ip = lines[1]
print 'Hue Bridge IP: ' + bridge_ip

b = Bridge(bridge_ip)
wiimote_connected = False

#Attempt to connect wiimote until successful
while wiimote_connected == False:
    print "press 1 + 2 now"
    try:
        # attempt to connect wii remote
        wm = cwiid.Wiimote()
        print "wiimote found"
        # set buttons to report when pressed
        wm.rpt_mode = cwiid.RPT_BTN
        wm.led = 1
        wiimote_connected = True
    except (RuntimeError, NameError):
        print "failed to find wiimote, retrying"

#dictionary for program use
dict = {'start' : 0, 'end' : 0, 'room1' : [], 'room2' : [], 'bright' : 0, 'group_state' : True, 'room_name': '', 'timer' : 0, 'repeat_cycle' : True}

#START DEFINING ROOMS from config
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

def check_bat(wm):
    #ensure battery is not to low
    battery_stat = wm.state['battery']
    if battery_stat <= 10:
        print 'remote disconnected due to low battery'
        wm.close()
        dict['timer'] = 0
        dict['repeat_cycle'] = False

def rumble(wm):
    #make wiimote rumble
    wm.rumble = True
    time.sleep(.1)
    wm.rumble = False

def change_lights(wm):
    #change state of hue light based upon the light thats on on the wii remote
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
        #if no lights with a set number are found this is pulled
        print 'no attached light'
        rumble(wm)
        rumble(wm)

def led_increase(wm):
    #change wii remote leds
    led_state = wm.state['led']
    if led_state >= 16:
        wm.led = 0
    else:
        wm.led = led_state + 1

def check_leds(wm):
    #check that the leds are not above the ones that are on the wiiremote
    if wm.state['led'] >= 16:
        wm.led = 15
    if wm.state['led'] <= 1:
        wm.led = 1

def checkset_bright(wm):
    #change hue light brightness
    if dict['bright'] >= 250:
        dict['bright'] = 254
    if dict['bright'] <= 25:
        dict['bright'] = 0
    light_number = wm.state['led']
    b.set_light(light_number, 'bri', dict['bright'])

def change_group_light():
    #change hue lights that are assigned to a room
    light_set = dict[dict['room_name']]
    #light_set = dict[indict]
    if dict['group_state'] == True:
        b.set_light(light_set, 'on', False)
        dict['group_state'] = False
    elif dict['group_state'] == False:
        b.set_light(light_set, 'on', True)
        dict['group_state'] = True

def check_light_state(wm):
    #check state of the hue lights and then give feedback on wiimote, flash twice for on and once for off
    led_num = wm.state['led']
    led_state = b.get_light(led_num, 'on')
    if led_state == True:
        wm.led = 15
        time.sleep(1)
        wm.led = 0
        time.sleep(1)
        wm.led = 15
        time.sleep(1)
        wm.led = 0
        time.sleep(1)
        wm.led = 1

    if led_state == False:
        wm.led = 15
        time.sleep(1)
        wm.led = 0
        time.sleep(1)
        wm.led = 1

    wm.led = led_num

def read_btns(wm):
    #read wii remote buttons
    #UP
    if (wm.state['buttons'] & cwiid.BTN_RIGHT):
        wm.led = wm.state['led'] + 1
        rumble(wm)
        check_leds(wm)


    #DOWN
    if (wm.state['buttons'] & cwiid.BTN_LEFT):
        wm.led = wm.state['led'] - 1
        rumble(wm)
        check_leds(wm)


    #A
    if (wm.state['buttons'] & cwiid.BTN_A):
        change_lights(wm)
        rumble(wm)

    #B
    if (wm.state['buttons'] & cwiid.BTN_B):
        check_light_state(wm)


    #LEFT
    if (wm.state['buttons'] & cwiid.BTN_DOWN):
        dict['bright'] = dict['bright'] - 50
        checkset_bright(wm)
        rumble(wm)


    #RIGHT
    if (wm.state['buttons'] & cwiid.BTN_UP):
        dict['bright'] = dict['bright'] + 50
        checkset_bright(wm)
        rumble(wm)


    #ONE
    if (wm.state['buttons'] & cwiid.BTN_1):
        dict['room_name'] = 'room1'
        change_group_light()
        rumble(wm)


    #TWO
    if (wm.state['buttons'] & cwiid.BTN_2):
        dict['room_name'] = 'room2'
        change_group_light()
        rumble(wm)

    check_bat(wm)

    #HOME
    if (wm.state['buttons'] & cwiid.BTN_HOME):
        print 'remote diconnected manually'
        rumble(wm)
        wm.close()
        dict['timer'] = 0
        dict['repeat_cycle'] = False

while True:
    #a timer that is used to disconnect the wiimote
    if dict['repeat_cycle'] == True:
        read_btns(wm)
        dict['timer'] += 1

    #Thats about an hour of inactivity till it disconnects
    if dict['timer'] >= 10000000:
        dict['timer'] = 0
        wm.close()
        print "remote disconnected due to inactivity"
        dict['repeat_cycle'] = False

    #if the wii remote disconnects this starts and continues to look for a new wiiremote and trys to attach it
    if dict['repeat_cycle'] == False:
        print 'looking for remote'
        try:
            # attempt to connect wii remote
            wm = cwiid.Wiimote()
            print "wiimote found"
            time.sleep(2)
            # set buttons to report when pressed
            wm.rpt_mode = cwiid.RPT_BTN
            wm.led = 1
            dict['repeat_cycle'] = True
        except (RuntimeError, ValueError):
            print "failed to find wiimote"

        time.sleep(.1)
