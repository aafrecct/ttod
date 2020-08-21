from curses import wrapper
from yaml import safe_load, dump

with open('options.yaml', 'r') as options_file:
    options = safe_load(options_file)

with open('./translations/en/tui_dialogs.yaml') as dialogs_file:
    dialogs = safe_load(dialogs_file)

def centered_string(s, stdscr):
    '''Takes a multiline string and adds it centered in stdscr.

    Arguments:
    s -- The string to add.
    stdscr -- The curses screen.
    '''
    rows, cols = stdscr.getmaxyx()
    # How many lines the string has.
    s = s.splitlines()
    str_h = len(s)
    # How many characters the lonest line has.
    ns = s.copy()
    ns.sort(key=lambda x:len(x))
    str_w = len(ns[-1])
    # Set begin and end of string
    begin_y, begin_x = (int((max_len - str_len) / 2) 
            for max_len, str_len in [(rows, str_h), (cols, str_w)])
    # Rebuild string
    s = "\n".join([(' ' * begin_x) + l for l in s])

    stdscr.addstr(begin_y, 0, s)


def main(stdscr):
    # Clear the screen.
    stdscr.clear()

    title = dialogs['title']
    centered_string(title, stdscr)
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
