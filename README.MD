# CircuitPython implementation of the Conway's Game Of Life

## Hardware

Implementation was tested in CircuitPython 5.2 on:
* PewPew M4 https://www.makerfabs.com/circuitpython-pewpew-m4.html
* Adafruit PyBadge LC https://www.adafruit.com/product/3939

![Pew Pew M4](/images/pewpewm4_gol.jpg)

## Configuration

It is possible to configure the following simulation parameters by editing constants near the top of the code.py file:
* behavior of the cells at the edge of the screen: if ROUND_WORLD has value True cells from first column / row will interact with cells from last column / row; if ROUND_WORLD has value False edge of the screen is recognized as a dead cell
* if USE_USER_SEED has value True USER_SEED will be used to seed the world with live cells at the beginning of the simulation; USE_USER_SEED has value False random seed will be generated and printed into serial console
* fraction of the screen seeded at the beginning og the simulation is defined by SIZE_OF_INITIAL_COLONY
* BACKGROUND_COLOUR and LIVE_CELL_COLOUR can be used to define background and live cell colour in HTML format; at the time of writing red and blue channels are switched in case of the PewPew M4
* UPDATE_DELAY can be used to slow down the simulation, it's the sleep time in seconds between the consecutive state calculations

## Warning

Although it's possible I don't recommend changing WORLD_WIDTH, WORLD_HEIGHT and CELL_SIZE parameters. A lot of memory is used for calculations and higher cells count can result in memory error.
