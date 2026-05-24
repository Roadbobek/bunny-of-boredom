# Python 3.14

import os
import sys
import time
import random
import socket
import textwrap
import threading

HOST = "127.0.0.1"
PORT = 33742

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

def add_horizontal_padding(content):
    # 1. Wrap text. We use a max width (e.g., 60) so it stays in a readable block
    # but ensure it doesn't exceed the actual terminal width.
    wrap_width = min(cli_size[0] - 2, 60)
    wrapped = textwrap.wrap(text.strip(), width=wrap_width) if text.strip() else []

    all_lines = []
    sprite_width = bnuy_size[0]

    # 2. Add text lines, calculating a custom offset to center each over the sprite
    for line in wrapped:
        # Center offset: Start of sprite + (half of sprite width) - (half of text line width)
        offset = target_col + (sprite_width - len(line)) // 2
        # Clamp the offset so text stays within terminal bounds [0, max_possible_pos]
        offset = max(0, min(offset, cli_size[0] - len(line)))
        all_lines.append(" " * offset + line)

    if wrapped:
        # Add a speech pointer '\/' centered over the bunny's head
        pointer_offset = target_col + (sprite_width // 2) - 1
        all_lines.append(" " * pointer_offset + r"\/")
        all_lines.append("") # Spacer line between text and sprite

    # 3. Add sprite lines using the standard target_col
    sprite_padding = " " * target_col
    for line in content.splitlines():
        all_lines.append(sprite_padding + line)

    # 4. Calculate the dynamic row so the bunny stays at the bottom
    dynamic_row = cli_size[1] - len(all_lines) + 1
    return f"\033[{dynamic_row};1H" + "\n".join(all_lines)

bnuy_size = (17, 5) # (width, height)

try: # cli_size == (width, height)
    cli_size = (os.get_terminal_size().columns, os.get_terminal_size().lines)
except: # assume user is running in an ide and assign standard values
    cli_size = (120, 30)

clear_cli()
hide_cursor()
# available space
horizontal_space = cli_size[0] - bnuy_size[0]

# horizontal spacing
target_col = random.randint(0, horizontal_space)

# horizontal bounds
# if target_col + bnuy_size[0] > cli_size[0]:
#     target_col = cli_size[0] - bnuy_size[0]
# get bnuy sprite, random direction
if random.choice([True, False]):
    sprite = bnuy_flip
    dir = 1
else:
    sprite = bnuy
    dir = 0

text = ""

def socket_listener():
    global text
    global running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow immediate reuse of the port after restart
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    new_msg = data.decode('utf-8').strip()
                    if new_msg:
                        if new_msg == "/cls":
                            text = ""
                        elif new_msg == "/shutdown":
                            running = False
                        else:
                            text = new_msg

# start the networking thread as a daemon so it closes when the main script ends
threading.Thread(target=socket_listener, daemon=True).start()

# show initial bnuy sprite
print(add_horizontal_padding(sprite), end="")

moving = False
stepping = True
wait = random.randint(10, 50)
blink_wait_time = 40
blink_wait = blink_wait_time
running = True
while running:
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
                if stepping:
                    sprite = bnuy_walk_flip
                    stepping = False
                else:
                    sprite = bnuy_flip
                    stepping = True
                print(add_horizontal_padding(sprite), end="")
                dir = 1
            elif target_col > new_pos:
                target_col -= 1
                if stepping:
                    sprite = bnuy_walk
                    stepping = False
                else:
                    sprite = bnuy
                    stepping = True
                print(add_horizontal_padding(sprite), end="")
                dir = 0
            else: # finished moving
                moving = False
                stepping = True
                wait = random.randint(10, 100)
    else:
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
        print(add_horizontal_padding(sprite), end="")
        blink_wait -= 1
    wait -= 1
