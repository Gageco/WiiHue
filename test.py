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
