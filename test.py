f = open("./config.py")
lines = f.readlines()
f.close()

dict = {'start' : 0, 'end' : 0}

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

while eval_line_txt != dict['end'] - 1:
    eval_line_txt += 1
    print eval(lines[eval_line_txt])
