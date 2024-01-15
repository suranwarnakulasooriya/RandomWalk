# RandomWalk
A terminal-based screen saver using random walks written in Python.

## Dependencies
The screen saver requires `curses` and `python3.10+`. Python can be downloaded from [python.org](https://www.python.org/downloads/) and `curses` can be installed with `pip`:
```
pip install curses
```

## Arguments
All of the following arguments are optional:
|Abbreviation|Name|Description|Default|Range|
|------------|----|-----------|-------|-----|
|-n|--walkers|number of random walkers|7|[1-7]|
|-b|--bias|bias to stay in the same direction|1|[0-100]|
|-nw|--nowrap|make walkers incapable of wrapping around the screen|
|-fps|--framerate|target frame rate|60|[10-500]|
|-h|--help|show the help message|

For example:
```
python3.10 randomwalk.py -n 5 --framerate 100 # 5 walkers at 100 FPS
```

## Controls
|Key|Action|
|---|------|
|q or ctrl+C|exit|
|space|pause|
|r|restart|
