import board
import displayio
import random
from time import sleep

# Options
ROUND_WORLD = True   # if True object can move around edges, if False edge is treated as an empty cell
USE_USER_SEED = False   # if True USER_SEED will be used to settle cells on world map, if False random seed will be generated
USER_SEED = 553443   # seed for the initial colony of cells
BACKGROUND_COLOUR = 0x000000
LIVE_CELL_COLOUR = 0x0070ff
SIZE_OF_INITIAL_COLONY = 0.4   # where 1 is the whole map
UPDATE_DELAY = 0   # additional delay between population updates

# Constants
WORLD_WIDTH = 40   # number of cells horizontally
WORLD_HEIGHT = 32   # number of cells vertically
CELL_SIZE = 4   # side of single cell in pixels
CENTER_X = int(WORLD_WIDTH / 2)
CENTER_Y = int(WORLD_HEIGHT / 2)

# Variables
cells = []   # array where Cell objects will be stored

display = board.DISPLAY
 
# Create a bitmap with two colours
bitmap = displayio.Bitmap(display.width, display.height, 2)
 
# Create a two colour palette
palette = displayio.Palette(2)
palette[0] = BACKGROUND_COLOUR
palette[1] = LIVE_CELL_COLOUR
 
# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
 
# Create a Group
group = displayio.Group()
 
# Add the TileGrid to the Group
group.append(tile_grid)
 
# Add the Group to the Display
display.show(group)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.live = False

    def change_state(self):   # changes state of the cell to opposite
        self.live = not self.live
        if self.live:
            draw_cell(self.x, self.y, 1)
        else:
            draw_cell(self.x, self.y, 0)

    def check_neighbours(self):
        self.live_neighbours = 0
        x_to_check = [self.x]
        y_to_check = [self.y]
        if ROUND_WORLD:
            y_to_check.append((self.y - 1) % WORLD_HEIGHT)
            y_to_check.append((self.y + 1) % WORLD_HEIGHT)
            x_to_check.append((self.x - 1) % WORLD_WIDTH)
            x_to_check.append((self.x + 1) % WORLD_WIDTH)
        else:
            if self.y > 0:   # if cell is in the row 0, it doesn't have neighbours above
                y_to_check.append(self.y - 1)
            if self.y < WORLD_HEIGHT - 1:   # if cell is in the lowest row, it doesn't have neighbours below
                y_to_check.append(self.y + 1)
            if self.x > 0:   # if cell is in the left column, it doesn't have neighbours from the left side
                x_to_check.append(self.x - 1)
            if self.x < WORLD_WIDTH - 1:   # if cell is in the right column, it doesn't have neighbours from the right side
                x_to_check.append(self.x + 1)
        for y in y_to_check:
            for x in x_to_check:
                if y != self.y or x != self.x:
                    if cells[x][y].live == True:
                        self.live_neighbours += 1

    def check_rules(self):
        if self.live == True:
            if self.live_neighbours < 2 or self.live_neighbours > 3:
                self.change_state()
        if self.live == False and self.live_neighbours == 3:
            self.change_state()

# Helper function used to draw single cell
def draw_cell(x, y, colour):
    for x_value in range(x * CELL_SIZE, x * CELL_SIZE + CELL_SIZE):
        for y_value in range(y * CELL_SIZE, y * CELL_SIZE + CELL_SIZE):
            bitmap[x_value, y_value] = colour

# Create world filled with dead cells
def create_world():
    global cells
    for x in range(0, WORLD_WIDTH):
        cells.append([])
        for y in range(0, WORLD_HEIGHT):
            cells[x].append(Cell(x, y))

# Randomize initial state
def seed_world():
    global cells
    randomized_seed = ''
    if USE_USER_SEED:
        print("User seed used: ", USER_SEED)
        random.seed(USER_SEED)
    else:
        for counter in range(0, 6):
            randomized_seed += str(random.randrange(0, 10))
        print("Seed used: ", randomized_seed)
        random.seed(int(randomized_seed))
    for y in range(int(CENTER_Y - SIZE_OF_INITIAL_COLONY * CENTER_Y),
                   int(CENTER_Y + SIZE_OF_INITIAL_COLONY * CENTER_Y)):
        for x in range(int(CENTER_X - SIZE_OF_INITIAL_COLONY * CENTER_X),
                       int(CENTER_X + SIZE_OF_INITIAL_COLONY * CENTER_X)):
            finger_of_god = random.randrange(0, 2)
            if finger_of_god == 1:
                cells[x][y].change_state()

# Helper function used to update state of the colony
def update_colony():
    for row in cells:
        for cell in row:
            cell.check_neighbours()
    for row in cells:
        for cell in row:
            cell.check_rules()

# Run the simulation
create_world()
seed_world()
while True:
    update_colony()
    sleep(UPDATE_DELAY)

