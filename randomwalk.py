# DEPENDENCIES ====================================================================================

import curses # for i/o
from random import randint,choice,shuffle # to generate random apple position
from datetime import datetime # to manage frame rate
from time import sleep #      ^
import argparse # to parse

# PARSE ARGS ======================================================================================

parser = argparse.ArgumentParser(prog='RandomWalk',
    description='A terminal-based screen saver using random walks written in Python.')

parser.add_argument('-n','--walkers',type=int,default=7,help='number of random walkers [1 to 7]')
parser.add_argument(
    '-b','--bias',type=int,default=1,help='bias to stay in the same direction [0 to 100]')
parser.add_argument('-nw','--nowrap',type=bool, 
action=argparse.BooleanOptionalAction,help='make walkers incapable of wrapping around the screen')
parser.add_argument('-fps','--framerate',type=int,default=60,help='target frame rate [10 to 500]')

args = parser.parse_args(); walkers:int = args.walkers; samedir_bias:int = args.bias
wrap:bool = not args.nowrap; target_fps:int = args.framerate

# FUNCTIONS =======================================================================================

def init_dimens(screen:curses.window) -> (bool,int,int): # get dimensions of game from terminal
    h,w = screen.getmaxyx()[0],screen.getmaxyx()[1]; f:bool = True
    if w < 25 or h < 25: f = False # the screen is not functional if the dimensions are too small
    return f,w,h # return whether the screen is big enough and dimens

def random_pos(a:int,b:int) -> (int,int): # return random coords
    x,y = randint(0,a-1),randint(0,b-1); return [y,x]

def close(scr:curses.window) -> None: # end curses and python
    scr.keypad(0); curses.nocbreak(); curses.endwin(); exit()

def reset(colors:list[int]):
    dirs = [choice(['u','d','l','r']) for _ in range(walkers)]; shuffle(colors)
    return [[0,0,0]*w for _ in range(h)], dirs, dirs[:], [random_pos(w,h) for _ in range(walkers)]

# SETUP ===========================================================================================

if __name__ == '__main__':

    # i/o setup
    stdscr:curses.window = curses.initscr()
    curses.start_color(); curses.use_default_colors() # use ansi colors
    curses.cbreak(); curses.noecho(); stdscr.nodelay(True) # make getch() nonblocking
    curses.curs_set(0); stdscr.keypad(True) # hide mouse and allow keyboard input

    paused:bool = False
    f,w,h = init_dimens(stdscr) # get dimens
    grid:list[list[(str,int,int)]] = [[0,0,0]*w for _ in range(h)] # empty grid

    color_lookup = {1:curses.COLOR_RED, 2:curses.COLOR_GREEN, 3:curses.COLOR_YELLOW,
            4:curses.COLOR_BLUE, 5:curses.COLOR_MAGENTA, 6:curses.COLOR_CYAN, 7:curses.COLOR_WHITE}
                    
    for i in range(1,8): curses.init_pair(i,color_lookup[i],-1) # generate ansii colors

    walkers:int = max(1,min(7,walkers)); samedir_bias:int = max(0,min(100,samedir_bias)) # clamp
    target_fps = max(10,min(500,target_fps)); target_frametime = 1/target_fps
    
    list_colors:list[int] = [_ for _ in range(0,7)]; shuffle(list_colors) # list of ansii colors
    list_d:list[str] = [choice(['u','d','l','r']) for _ in range(walkers)] # directions of walkers
    list_walkers:list[[int,int]] = [random_pos(w,h) for _ in range(walkers)] # walker positions
    list_prevd:list[str] = list_d[:] # list of previous walker positions
    length:int = w*h//(3+walkers) # maximum length of a walker's path before it starts clearing


# EVENT LOOP ======================================================================================

while __name__ == '__main__':
    try:
        # INPUT ===================================================================================

        dt1 = datetime.now() # get current time
        input_char = stdscr.getch(); stdscr.erase() # get input and clear screen

        if input_char == curses.KEY_RESIZE: # reset game if window is resized
            f,w,h = init_dimens(stdscr); # get new dimens
            grid, list_d, list_prevd, list_walkers = reset(list_colors) # reset on resize
            stdscr.clear(); stdscr.refresh() # clear screen
            length = w*h//(3+walkers) # set new length for new dimens

        elif input_char == ord('q'): close(stdscr) # quit on q
        elif input_char == ord(' '): paused ^= 1 # toggle pause on space
        elif input_char == ord('r'): grid, list_d, list_prevd, list_walkers = reset(list_colors)

        for i,d in enumerate(list_d):
            if   d == 'u': list_d[i] = choice(['u']*samedir_bias*(wrap or list_walkers[i][0] != 0)
            + ['l']*(wrap or list_walkers[i][1] != 0) + ['r']*(wrap or list_walkers[i][1] != w-1))
            elif d == 'd': list_d[i] = choice(['d']*samedir_bias*(wrap or list_walkers[i][0]!= h-1)
            + ['l']*(wrap or list_walkers[i][1] != 0) + ['r']*(wrap or list_walkers[i][1] != w-1))
            elif d == 'l': list_d[i] = choice(['l']*samedir_bias*(wrap or list_walkers[i][1] != 0)
            + ['u']*(wrap or list_walkers[i][0] != 0) + ['d']*(wrap or list_walkers[i][0] != h-1))
            elif d == 'r': list_d[i] = choice(['r']*samedir_bias*(wrap or list_walkers[i][1]!= w-1)
            + ['u']*(wrap or list_walkers[i][0] != 0) + ['d']*(wrap or list_walkers[i][0] != h-1))

        # RANDOM WALK =============================================================================

        if not paused:
            for i in range(walkers):
                walker = list_walkers[i]; prevp = walker; d = list_d[i]; prevd = list_prevd[i]
                
                if d == 'u': 
                    walker[0] -= 1
                    if walker[0] == -1: list_walkers[i][0] = h-1
                        
                    try:
                        if prevd == 'u':grid[prevp[0]+1][prevp[1]] = ['┃',list_colors[i],length]
                        elif prevd == 'l': grid[prevp[0]+1][prevp[1]] = ['┗',list_colors[i],length]
                        elif prevd == 'r': grid[prevp[0]+1][prevp[1]] = ['┛',list_colors[i],length]
                    except:
                        if prevd == 'u':grid[0][prevp[1]] = ['┃',list_colors[i],length]
                        elif prevd == 'l': grid[0][prevp[1]] = ['┗',list_colors[i],length]
                        elif prevd == 'r': grid[0][prevp[1]] = ['┛',list_colors[i],length]

                elif d == 'd':
                    walker[0] += 1
                    if walker[0] == h: list_walkers[i][0] = 0

                    if prevd == 'd': grid[prevp[0]-1][prevp[1]] = ['┃',list_colors[i],length]
                    elif prevd == 'l': grid[prevp[0]-1][prevp[1]] = ['┏',list_colors[i],length]
                    elif prevd == 'r': grid[prevp[0]-1][prevp[1]] = ['┓',list_colors[i],length]

                elif d == 'l':
                    walker[1] -= 1
                    if walker[1] == -1: list_walkers[i][1] = w-1

                    try:
                        if prevd == 'u': grid[prevp[0]][prevp[1]+1] = ['┓',list_colors[i],length]
                        elif prevd == 'd': grid[prevp[0]][prevp[1]+1] = ['┛',list_colors[i],length]
                        elif prevd == 'l': grid[prevp[0]][prevp[1]+1] = ['━',list_colors[i],length]
                    except:
                        if prevd == 'u': grid[prevp[0]][0] = ['┓',list_colors[i],length]
                        elif prevd == 'd': grid[prevp[0]][0] = ['┛',list_colors[i],length]
                        elif prevd == 'l': grid[prevp[0]][0] = ['━',list_colors[i],length]

                elif d == 'r':
                    walker[1] += 1
                    if walker[1] == w: list_walkers[i][1] = 0

                    if prevd == 'u': grid[prevp[0]][prevp[1]-1] = ['┏',list_colors[i],length]
                    elif prevd == 'd': grid[prevp[0]][prevp[1]-1] = ['┗',list_colors[i],length]
                    elif prevd == 'r': grid[prevp[0]][prevp[1]-1] = ['━',list_colors[i],length]
                    
                list_prevd[i] = d

        # OUTPUT ==================================================================================

        if f: # if the screen is big enough to draw on
            for r in range(h):
                for c in range(w):
                    if grid[r][c]: # if the grid position has a line segment
                        try: # draw line segment
                            stdscr.addstr(r,c,grid[r][c][0],curses.color_pair(grid[r][c][1]+1))
                            if not paused: # reduce length of line segment
                                grid[r][c][2] -= 1
                                if grid[r][c][2] == 0: grid[r][c] = 0
                        except: pass
            
        else: stdscr.addstr('Window is not big enough (need at least 25x25).') # error text

        sleep(max(0,target_frametime-(datetime.now()-dt1).microseconds/1e6)) # maintain frame rate
        #stdscr.addstr(0,0,str(round(1/((datetime.now()-dt1).microseconds/1e6),1))) # show fps
        stdscr.refresh()

    except KeyboardInterrupt: close(stdscr) # quit on ^C
