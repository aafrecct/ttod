import curses as crs
from yaml import safe_load, dump

key = ""

with open('options.yaml', 'r') as options_file:
    options = safe_load(options_file)

with open('./translations/en/tui_dialogs.yaml', 'r') as dialogs_file:
    dialogs = safe_load(dialogs_file)


def print_string(y, x, s, win):
    '''Takes a list of strings and adds it to the window given.

    Arguments:
    y   -- The y coordinate.
    x   -- The x coordinate.
    s   -- The list of strings.
    win -- The window to add the string to.
    '''
    # How many lines the string has.
    str_h = len(s)
    # How many characters the lonest line has.
    ns = sorted(s.copy(), key=len)
    str_w = len(ns[-1])
    # Print string.
    for i in range(len(s)):
        win.addstr(y + i, x, s[i])


def centered_string(s, win):
    '''Takes a list of strings and adds it centered in win.

    Arguments:
    s -- The list of strings to add.
    win -- The curses window.
    '''
    rows, cols = win.getmaxyx()
    # How many lines the string has.
    str_h = len(s)
    # How many characters the lonest line has.
    ns = sorted(s.copy(), key=len)
    str_w = len(ns[-1])
    # Set begin and end of string.
    y, x = (int((max_len - str_len) / 2) 
            for max_len, str_len in [(rows, str_h), (cols, str_w)])
    print_string(y, x, s, win)


def right_side(s, win):
    '''Takes a list of strings and adds it in the right side of scr.
    It splits the width of scr with a 13:7 ratio.

    Arguments:
    s -- The list of strings to add.
    win -- The curses window.
    '''
    rows, cols = win.getmaxyx()
    # How many lines the string has.
    str_h = len(s)
    # How many characters the lonest line has.
    ns = sorted(s.copy(), key=len)
    str_w = len(ns[-1])
    # Set begin and end of string.
    y, x = (int((max_len - str_len) / 2) 
            for max_len, str_len in [(rows, str_h), (int(13 * cols / 20), str_w)])
    print_string(y, x, s, win)


def update_left_menu(s, win, selected_option = 0):
    '''Takes a list of strings and adds it in the left side of scr.
    It splits the width of scr with a 13:7 ratio.
    It 'selects' the option with index given.

    Arguments:
    s               -- The list of strings to add.
    win             -- The curses window.
    selected_option -- The option to mark as selected.
    '''
    for i in range(len(s)):
        if i == selected_option:
            s[i] = "> " + s[i][2:-2] + " <"
        else:
            s[i] = "  " + s[i][2:-2] + "  "

    rows, cols = win.getmaxyx()
    # How many lines the string has.
    str_h = len(s)
    # How many characters the lonest line has.
    ns = sorted(s.copy(), key=len)
    str_w = len(ns[-1])
    # Set begin and end of string.
    y, x = (int((max_len - str_len) / 2) 
            for max_len, str_len in [(rows, str_h), (int(7 * cols / 20), str_w)])
    print_string(y, x + int(13 * cols / 20), s, win)
    

def magage_left_menu(menu, win):
    selected_option = 0
    pressed_key = None
    selection_keys = [o[o.index('[') + 1] for o in menu]
    selection_keys.append('\n')

    while pressed_key not in selection_keys:
        if pressed_key == 'KEY_DOWN':
            selected_option += 1 if selected_option < len(menu) - 1 else 0
        elif pressed_key == 'KEY_UP':
            selected_option -= 1 if selected_option > 0 else 0
        update_left_menu(menu, win, selected_option)
        win.refresh()
        pressed_key = win.getkey()

    return None


def main(stdscr):
    # Clear the screen.
    stdscr.clear()

    # Display game title.
    title = dialogs['title']
    centered_string(title, stdscr)
    stdscr.refresh()
    
    # Next screen
    stdscr.getkey()
    stdscr.clear()

    # Main menu
    right_title = dialogs['title_compact']
    right_side(right_title, stdscr)
    main_menu = dialogs['main_menu']
    magage_left_menu(main_menu, stdscr)
    stdscr.refresh()
    
    #global key    
    #key = stdscr.getkey()

crs.wrapper(main)
#print(repr(key))
