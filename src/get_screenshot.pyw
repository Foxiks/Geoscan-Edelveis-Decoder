import win32gui, sys

def get_pos(name):
    try:
        window_handle = win32gui.FindWindow(None, name)
        rect = win32gui.GetWindowRect(window_handle)
        x=rect[0]+4
        y=rect[1]+1
        w=int(rect[2]-x)-4
        h=int(rect[3]-y)-2
        return [x,y,w,h]
    except win32gui.error:
        return 1

def main():
    pos=get_pos("[GUI] Geoscan-Edelveis Decoder by Egor UB1QBJ (Ver. 1.3.1)")
    if(pos!=1):
        with open('pos.txt', 'w') as f:
            f.write(str(pos[0])+'\n'+str(pos[1])+'\n'+str(pos[2])+'\n'+str(pos[3]))
    else:
        sys.exit()

if __name__ == '__main__':
    main()