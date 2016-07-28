f = open("./config.py")
lines = f.readlines()
f.close()

x = 0
for txt_line in lines:
    try:
        print x
        txt = eval(lines[x])
        if txt == 'START':
            print "found start"
            print x
        if txt =='END':
            print 'found end'
            print x
    except SyntaxError:
        pass
    x += 1
