#!/usr/bin/env python3
# Jayden W

# import libs
import random
import PIL.Image

# TODO - Stitch together smaller mazes to create much larger mazes

'''
Progress does not accurately represent time remaining
expect progress to slow as it reaches the end
'''
show_progress = True
create_background = True

'''
generates some % of the maze, in case it takes too long
100 for full maze generation
'''
fast_gen = 100
# color theme
dark_mode = True

'''
dimensions and cell sizes
all measured in pixels
'''
size = 100
cell_size = 3

# colors
if not dark_mode:
    WALL = (0, 0, 0, 255)
    CELL = (255, 255, 255, 255)
else:
    # inverted
    CELL = (0, 0, 0, 255)
    WALL = (255, 255, 255, 255)

# declare global variables
attempts = 4
visited = set()
vis_l = []

# match cell_size to pixel size
cell_size += 1
# create an empty canvas for the maze
maze = PIL.Image.new(mode="RGB", size=(size * cell_size + 1, size * cell_size + 1), color=WALL)

# four cardinal directions
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def is_perimeter(x: int, y: int) -> bool:
    return x == 0 or x * cell_size == size - 1 or y == 0 or y * cell_size == size - 1

# draw a cell_size x cell_size 'pixel' (cell)
def draw_pixel(i : int, j : int, c : tuple[int, ...]) -> None:
    for offsetx in range(1, cell_size):
        for offsety in range(1, cell_size):
            maze.putpixel((i * cell_size + offsetx, j * cell_size + offsety), c)

# draw the base(grid) the maze is drawn on
def draw_grid() -> None:
    for i in range(size):
        for j in range(size):
            # draw the pixel at position i, j
            draw_pixel(i, j, CELL)

# remove the wall at cell (i, j)
def erase_wall(i: int, j: int, v: bool, color: tuple[int, ...]) -> None:
    # loop cell_size times for an edge
    for m in range(1, cell_size):
        maze.putpixel((i * cell_size + m * v, j * cell_size + m * (not v)), color)

# quick and dirty way to locate an empty cell (pixel)
def find_empty_cell() -> tuple[int, ...]:
    # for each of the columns
    for i in range(size):
        # for each of the rows
        for j in range(size):
            # if the pixel is free
            if not (i, j) in vis_l:
                # return the location
                return (i, j)
    # no empty spaces
    return (-1, -1)

# return a random color
def return_random_color() -> tuple[int, ...]:
    rng = random.randint
    return (rng(0, 255), rng(0, 255), rng(0, 255), 255)

def remove_wall(x: int, y: int, direction: str, color: tuple[int, ...]) -> None:

    match direction:

        # case "up": erase_wall(x, y, 1, color)
        case 0: erase_wall(x, y, 1, color)

        # case "right": erase_wall(x + 1, y, 0, color)
        case 1: erase_wall(x + 1, y, 0, color)

        # case "down": erase_wall(x, y + 1, 1, color)
        case 2: erase_wall(x, y + 1, 1, color)

        # case "left": erase_wall(x, y, 0, color)
        case 3: erase_wall(x, y, 0, color)

# return a random visited cell
def find_visited_cell() -> tuple[int, ...]:
    if len(visited) >= size ** 2:
        return (-1, -1)
    return random.choice(vis_l)

# change a color by a slight amount
def alter_color(color: tuple[int, ...], change: int) -> tuple[int, ...]:
    # change varies from 1 -> size ^ 2
    if (color[0] + color[1] + color[2] < 127):
        return (
            color[0] + (255 - color[0]) // change,
            color[1] + (255 - color[1]) // change,
            color[2] + (255 - color[2]) // change,
            255
        )
    else:
        return (
            color[0] - color[0] // change,
            color[1] - color[1] // change,
            color[2] - color[2] // change,
            255
        )

def DFS(start_cell: tuple[int, ...]) -> None:
    global visited; visited.add(start_cell)

    # create an *local* alias for random.randint
    rng = random.randint
    
    vis_l.append(start_cell)
    current_cell = start_cell
    found_path = True
    
    while found_path:
        found_path = False
        for _ in range(attempts):
            # direction, offsets = list(zip(names, directions))[rng(0, 3)]
            offsets = directions[index := rng(0, 3)]
            if 0 <= current_cell[0] + offsets[0] < size and 0 <= current_cell[1] + offsets[1] < size and not (new_cell := (current_cell[0] + offsets[0], current_cell[1] + offsets[1])) in visited:
                # valid path
                visited.add(new_cell)
                vis_l.append(new_cell)
                remove_wall(current_cell[0], current_cell[1], index, CELL)
                current_cell = new_cell
                found_path = True

# normalize to (0 -> 1)
def normalize(number, max_value, offset = 0) -> float:
    # offsets ensure no zero values
    return (number + offset) / (max_value + offset)

def create_gradient_bg() -> None:
    '''
    pixel_count = size * cell_size
    for col in range(pixel_count):
        for row in range(pixel_count):
            maze.putpixel((col, row), (int(normalize(col, pixel_count) * 255), int(normalize(row, pixel_count) * 255), int(normalize(col * row / 2, pixel_count) * 255)))
        if (percent := int(100 * (col / pixel_count))) != int(100 * ((col - 1) / pixel_count)) and show_progress:
            print(f"{percent}%")
    if show_progress: print(r"100% - Finished background")
    '''
    pixel_count = size * cell_size
    for col in range(pixel_count):
        for row in range(pixel_count):
            if is_perimeter(col, row):
                maze.putpixel((col, row), WALL)
            else:
                maze.putpixel(
                    (col, row),
                    (
                        int(normalize(col, pixel_count) * 255),
                        int(normalize(row, pixel_count) * 255),
                        int(normalize(255 - (row + col) * 0.5, 255) * 255)
                    )
                )
        if (percent := int(100 * (col / pixel_count))) != int(100 * ((col - 1) / pixel_count)) and show_progress:
            print(f"{percent}%")
    if show_progress: print(r"100% - Finished background")

def draw_maze():
    previous = 0
    
    DFS((0, 0))
    # loop random walks to create a maze
    while (empty_cell := find_visited_cell()) != (-1, -1):
        '''
        draw_pixel(0, 0, WALL)
        remove_wall(0, 0, "right", (255, 0, 0, 255))
        '''
        DFS(empty_cell)

        if show_progress and (percent := int(100 * len(visited)/size**2)) != previous:
            print(f"{percent}%")
            previous = percent
            if percent == fast_gen:
                break

def save_image():

    response = input("save this image? (y/n)")
    
    if response.lower() == "y":
    
        maze.save(f"Mazes/maze ({size} - {cell_size}{" BG" if create_background else ""}).png")


# run the program
if __name__ == "__main__":

    if create_background:
        create_gradient_bg()

    draw_grid()
    
    draw_maze()

    maze.show()
    
    save_image()
