import os
import sys
import time
import random
import textwrap

bnuy = r''' /\\=//\-"""-.
/_/o o\_\     \
 =\_Y_/=  (_  ;{}
   |^||_|-/__/
   "" ""  """'''

bnuy_walk = r''' /\\=//\-"""-.
/_/o o\_\     \
 =\_Y_/=  (_  ;{}
  /^//_/--|__|
  "" ""    """'''

bnuy_blink = r''' /\\=//\-"""-.
/_/- -\_\     \
 =\_Y_/=  (_  ;{}
   |^||_|-/__/
   "" ""  """'''

bnuy_walk_blink = r''' /\\=//\-"""-.
/_/- -\_\     \
 =\_Y_/=  (_  ;{}
  /^//_/--|__|
  "" ""    """'''

bnuy_flip = r'''   .-"""-/\\=//\
  /     /_/o o\_\
{};  _)  =\_Y_/=
   \__\-|_||^|
    """  "" ""'''

bnuy_walk_flip = r'''   .-"""-/\\=//\
  /     /_/o o\_\
{};  _)  =\_Y_/=
   |__|--\_\\^\
   """    "" ""  '''

bnuy_blink_flip = r'''   .-"""-/\\=//\
  /     /_/- -\_\
{};  _)  =\_Y_/=
   \__\-|_||^|
    """  "" ""'''

bnuy_walk_blink_flip = r'''   .-"""-/\\=//\
  /     /_/- -\_\
{};  _)  =\_Y_/=
   |__|--\_\\^\
   """    "" ""'''


def clear_cli():
    os.system('cls' if os.name == 'nt' else 'clear')

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def move_cursor(target_row: int):
    print(f"\033[{target_row};1H", end="")

def add_horizontal_padding(content):
    if text.strip():
        content = text.strip() + "\n\n" + content.format("")
    content = content[:0] + (" " * target_col) + content[0:]
    spacing = (" " * target_col)
    index = 0
    while index < len(content):
        if content[index] == '\n':
            content = content[:index + 1] + spacing + content[index + 1:]
            index += len(spacing)
        index += 1
    return content

bnuy_size = (17, 5) # (width, height)

try: # cli_size == (width, height)
    cli_size = (os.get_terminal_size().columns, os.get_terminal_size().lines)
except: # assume user is running in an ide and assign standard values
    cli_size = (120, 30)

clear_cli()
hide_cursor()

# # calculate the row to print the top of the text so the bnuy bottom aligns with the terminal bottom
# # bnuy_size[1] is the height of the bnuy character (5 lines) + 1 line for text
# target_row = cli_size[1] - bnuy_size[1]  # vertical alignment, bottom

# calculate the row to print the top of the bnuy character so its bottom aligns with the terminal bottom
# bnuy_size[1] is the height of the bnuy character (5 lines)
# cli_size[1] is the total height of the terminal
# we want the last line of bnuy to be on the last line of the terminal
# so, the first line of bnuy should be at cli_size[1] - bnuy_size[1] + 1
# the + 1 is because terminal rows start at 1, not 0
target_row = cli_size[1] - bnuy_size[1] + 1 # vertical alignment, bottom

# available space
horizontal_space = cli_size[0] - bnuy_size[0]

# horizontal spacing
target_col = random.randint(0, horizontal_space)

# horizontal bounds
# if target_col + bnuy_size[0] > cli_size[0]:
#     target_col = cli_size[0] - bnuy_size[0]

# move cursor to target_row, column 1, and print without new line
move_cursor(target_row)

# get bnuy sprite, random direction
if random.choice([True, False]):
    sprite = bnuy_flip
    dir = 1
else:
    sprite = bnuy
    dir = 0

text = "Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World! Hello, World!"
# text = ""

# add horizontal padding to sprite
sprite = add_horizontal_padding(sprite)

#print(repr(sprite) + "\n") # raw str representation

# show initial bnuy sprite
print(sprite, end="")

moving = False
stepping = True
wait = random.randint(10, 50)
blink_wait_time = 40
blink_wait = blink_wait_time
while True:
    time.sleep(0.05) # 20 fps
    clear_cli()

    if wait <= 0:
        if not moving:
            # new random position
            new_pos = random.randint(0, horizontal_space)
            moving = True
        else: # move to new pos
            if target_col < new_pos:
                target_col += 1
                move_cursor(target_row)
                if stepping:
                    sprite = bnuy_walk_flip
                    stepping = False
                else:
                    sprite = bnuy_flip
                    stepping = True
                sprite = add_horizontal_padding(sprite)
                print(sprite, end="")
                dir = 1
            elif target_col > new_pos:
                target_col -= 1
                move_cursor(target_row)
                if stepping:
                    sprite = bnuy_walk
                    stepping = False
                else:
                    sprite = bnuy
                    stepping = True
                sprite = add_horizontal_padding(sprite)
                print(sprite, end="")
                dir = 0
            else: # finished moving
                moving = False
                stepping = True
                wait = random.randint(10, 100)
    else:
        move_cursor(target_row)
        if dir == 0:
            if blink_wait > 0:
                sprite = bnuy
            else:
                sprite = bnuy_blink
                blink_wait = blink_wait_time
        else:
            if blink_wait > 0:
                sprite = bnuy_flip
            else:
                sprite = bnuy_blink_flip
                blink_wait = blink_wait_time
        sprite = add_horizontal_padding(sprite)
        print(sprite, end="")
        blink_wait -= 1
    wait -= 1