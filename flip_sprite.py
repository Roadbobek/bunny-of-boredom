def flip_ascii_sprite(sprite_str, width=17):
    # mapping of characters that need to be mirrored
    mirror_map = {
        '/': '\\', '\\': '/',
        '(': ')', ')': '(',
        '{': '}', '}': '{',
        '[': ']', ']': '[',
        '<': '>', '>': '<'
    }

    flipped_lines = []
    # split by newline, but handle potential empty lines from triple quotes
    for line in sprite_str.splitlines():
        # pad to fixed width so the 'box' flips correctly
        padded = line.ljust(width)
        # reverse the line
        reversed_line = padded[::-1]
        # mirror the directional characters
        flipped_line = "".join(mirror_map.get(c, c) for c in reversed_line)
        flipped_lines.append(flipped_line)

    return "\n".join(flipped_lines)


bnuy = r''' /\\=//\-"""-.
/_/o o\_\     \
 =\_Y_/=  (_  ;{}
   |^||_|-/__/
   "" ""  """'''

bnuy_walk = r''' /\\=//\-"""-.
/_/o o\_\     \
 =\_Y_/=  (_  ;{}
  /^//_/--\__\
  "" ""    """'''

bnuy_blink = r''' /\\=//\-"""-.
/_/- -\_\     \
 =\_Y_/=  (_  ;{}
   |^||_|-/__/
   "" ""  """'''

bnuy_walk_blink = r''' /\\=//\-"""-.
/_/- -\_\     \
 =\_Y_/=  (_  ;{}
  /^//_/--\__\
  "" ""    """'''

print(bnuy)
print(bnuy_walk)
print(bnuy_blink)
print(bnuy_walk_blink)

print()
print()
print()

print(flip_ascii_sprite(bnuy))
print(flip_ascii_sprite(bnuy_walk))
print(flip_ascii_sprite(bnuy_blink))
print(flip_ascii_sprite(bnuy_walk_blink))