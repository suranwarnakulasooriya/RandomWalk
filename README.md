# RandomWalk
A terminal-based screen saver using random walks written in Python.

# Dependencies
The screen saver requires `curses` and `python3.10+`. Python can be downloaded from [python.org](https://www.python.org/downloads/) and `curses` can be installed with `pip`:
```
pip install curses
```

# Configuration
The following values can be configured in `randomwalk.py`:
```
10 target_fps:int   = 60 # target frames per second
11 walkers:int      = 7 # number of random walkers [1 to 7]
12 samedir_bias:int = 10 # bias to stay in the same direction [0 to 100]
13 wrap:bool        = True # if paths can wrap around the screen
```
