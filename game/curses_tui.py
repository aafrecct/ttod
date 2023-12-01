import curses
from yaml import safe_load, dump
from textwrap import wrap
from game.player import Player
from game.tod_game import TODGame


class CursesTUI:
    """A class to display the game of Truth or Dare.
    Generally it divides the main screen in two sections:
        - A right side taking 65% of the width to display the questions
        and other game information.
        - A left side taking the rest that displays the menus of options
        to choose for.
    This is all handled in one window with a minimal aesthetic, no division
    between the two sides and written with a general "made for this game" attitude,
    meaning the code isn't very re-usable.

    Arguments:
        stdscr  -- A curses screen covering the screen.
        dialogs -- A dictionary corresponding to the file 'tui_dialogs' in a language.
    """

    class TextBox:

        def __init__(self, text, bound=0):
            if isinstance(text, str):
                self.lines = [text] if not bound else wrap(text, bound-2)
            elif isinstance(text, list):
                self.lines = text
            self.width = max(map(len, self.lines))
            self.height = len(self.lines)

    def __init__(self, screen, dialogs):
        self.screen = screen
        self.dialogs = dialogs
        self.height, self.width = self.screen.getmaxyx()
        self.left_width = int(13 / 20 * self.width)
        self.right_width = self.width - self.left_width

        self.screen.border("░")
        curses.use_default_colors()
        curses.curs_set(0)

    def clear(self):
        """Clears the screen"""
        self.screen.clear()

    def divide_screen():
        self.left_screen = curses.newwin(self.height, self.left_width)
        self.right_screen = curses.newwin(self.height, self.right_width, 0,
                                          self.left_width)

    def center_rectangle(self, window, height, width):
        """Calculates the coordinates of the top left corner for
        a rectangle of the size given to be centered in the screen"""
        window_height, window_width = window.getmaxyx()
        y = int((window_height - height) / 2)
        x = int((window_width - width) / 2)
        return y, x

    def paint_text(self, window, y, x, textbox):
        # Print string.
        for i, line in enumerate(textbox.lines):
            window.addstr(y + i, x, line)

    def paint_main_title(self):
        # How many lines the string has.
        titlecard = self.TextBox(self.dialogs['title'])
        # Set begin and end of string.
        y, x = self.center_rectangle(self.screen, titlecard.height, titlecard.width)
        self.paint_text(self.screen, y, x, titlecard)

    def paint_left(self, textbox):
        # Set begin and end of string.
        y, x = self.center_rectangle(self.left_screen, textbox.height,
                                textbox.width)
        self._paint_string(y, x, textbox.lines)

    def paint_left_lower(self, string):
        '''Takes a single string and adds it at the bottom of the left side of scr.'''
        y, x = (self.h - 2, int((self.w - len(s)) / 2))
        self._paint_string(y, x, s)

    def clear_left(self):
        '''Clears only the left side.'''
        self.paint_left([' ' * self._left_width() for i in range(self.h)])

    def paint_right(self, s):
        '''Takes a list of strings and adds it in the right side of scr.
        It splits the width of scr with a 13:7 ratio.
    
        Arguments:
        s               -- The list of strings to add.
        '''
        # How many lines the string has.

        str_h = len(s)
        # How many characters the lonest line has.
        ns = sorted(s.copy(), key=len)
        str_w = len(ns[-1])
        # Set begin and end of string.
        y, x = (int((max_len - str_len) / 2)
                for max_len, str_len in [(self.h,
                                          str_h), (self._right_width(),
                                                   str_w)])
        self._paint_string(y, x + self._left_width(), s)

    def clear_right(self):
        '''Clears only the right side.'''
        self.paint_right(['' * self._right_width() for i in range(self.h)])

    @staticmethod
    def _select_option(menu, selected_option=0):
        '''Adds '> ... <' marks to the selected_option in a list of strings.'''
        for i in range(len(menu)):
            if i == selected_option:
                menu[i] = "> " + menu[i][2:-2] + " <"
            else:
                menu[i] = "  " + menu[i][2:-2] + "  "
        return menu

    def _manage_right_menu(self, menu):
        '''A function to manage the options of the menu on the left.
        It returns the index of the selected option.

        Attributes:
        menu - A list of strings representing diferent options.
        '''
        selected_option = 0
        pressed_key = None
        selection_keys = [o[o.index('[') + 1].lower() for o in menu]
        selection_keys.append('\n')

        while pressed_key not in selection_keys:
            if pressed_key == 'KEY_DOWN':
                selected_option += 1 if selected_option < len(menu) - 1 else 0
            elif pressed_key == 'KEY_UP':
                selected_option -= 1 if selected_option > 0 else 0
            self.paint_right(self._select_option(menu, selected_option))
            self.scr.refresh()
            pressed_key = self.scr.getkey()

        if pressed_key == '\n':
            return selected_option
        else:
            return selection_keys.index(pressed_key)

    def paint_main_menu(self):
        '''Paints the smaller title on the right and
        returns the selected option in the main menu.'''
        self.paint_left(self.dialogs['compact_title'])
        return self._manage_right_menu(self.dialogs['main_menu'])

    def _handle_typing(self, shadow_str='', initial_str=''):
        '''Returns the word typed on the left side of the screen.'''
        # Store the typed string:
        typed = initial_str
        # Draw the shadow_str:
        self.clear_left()
        self.paint_left(shadow_str if initial_str == '' else initial_str)
        # Keep the last keypress:
        last_keypress = self.scr.getkey()
        # Until return is pressed:
        while last_keypress != '\n':
            if last_keypress == "KEY_BACKSPACE" and len(typed) != 0:
                typed = typed[:-1]
            elif len(last_keypress) == 1:
                typed += last_keypress
            self.clear_left()
            self.paint_left(typed)
            last_keypress = self.scr.getkey()
        # Return the typed string:
        return typed

    def _add_player(self):
        '''Returns a new Player object with the typed name'''
        # Call a method to type the name:
        player_name = self._handle_typing('Start typing a name')
        player = Player(player_name)
        return player

    def _pair_players(self):
        first = self._handle_typing('Type the index of first player')
        second = self._handle_typing('Type the index of second player')
        return (first, second)

    def _edit_player(self, players):
        i = self._handle_typing('Type the index of player to edit')
        if i not in [str(j) for j in range(len(players))]:
            return ()
        else:
            player = players[int(i)].name
            player = self._handle_typing(initial_str=player)
            return (int(i), player)

    def _del_player(self):
        return self._handle_typing('Type the index of player to delete')

    def paint_player_menu(self):
        '''Paints the screen to add the players to a new game.
        Returns the list of players.'''
        players = []
        option = -1
        # Prompt the user.
        self.paint_left("Add a player!")
        # Keep menu open until the game starts.
        while option != 4:
            # Get an option from the menu.
            option = self._manage_right_menu(self.dialogs['player_menu'])
            if option == 0:
                # Add the player typed in _add_player().
                players.append(self._add_player())
            elif option == 1:
                # Modify the player.partner atribute in two players.
                li = [str(i) for i in range(len(players))]
                partners = self._pair_players()
                if partners[0] in li and partners[1] in li:
                    i, j = int(partners[0]), int(partners[1])
                    players[i].partner, players[j].partner = players[
                        j], players[i]
            elif option == 2:
                # Edit the player.name attribute of the selected player.
                p = self._edit_player(players)
                if len(p) != 0:
                    players[p[0]].name = p[1]
            elif option == 3:
                # Remove the selcted player from the list of players.
                li = [str(i) for i in range(len(players))]
                p = self._del_player()
                if p in li:
                    players.pop(int(p))

            self.clear_left()
            # Add an indicator of the partners of each player.
            print_partners = [
                " ( ♡ " + p.partner.name +
                " )" if p.partner is not None else '' for p in players
            ]
            # Paint the full list of players.
            self.paint_left([
                str(i) + ") " + players[i].name + print_partners[i]
                for i in range(len(players))
            ])
        return players

    def paint_choice_menu(self, player):
        '''Displays the menu to decide between Truth or Dare and returns the selected choice.'''
        self.paint_left(player.name)
        return_list = ['truth', 'dare', 'random']
        return return_list[self._manage_right_menu(
            self.dialogs['choice_menu'])]

    def _process_question(self, question):
        '''Returns a list of strings representing the question given so that:
            - It fits on the left side.
            - The names are printed with the question.
        Arguments:
            question -- A tuple of the form (player, question, player, player)
                        where the first player is asked the question and the second
                        and third are their partner and a random player.
        '''
        string = question[1].format(question[0], question[2], question[3])
        max_len = self._left_width() - 2
        if len(string) < max_len:
            return [question[0] + ':', string]
        else:
            remain = string
            l = [question[0] + ':']
            while len(remain) > max_len:
                split = remain.rfind(' ', 0, max_len)
                l.append(remain[0:split])
                remain = remain[split + 1:]
            l.append(remain)
            return l

    def paint_question(self, question):
        self.paint_left(self._process_question(question))

    def paint_question_menu(self):
        return self._manage_right_menu(self.dialogs['question_menu'])

    def paint_player_below(self, player):
        self._paint_string(self.h - 2, 0, [" " * self._left_width()])
        player = player.name
        x = int((self._left_width() - len(player)) / 2)
        self._paint_string(self.h - 2, x, [player])

    def paint_random_number(self, number):
        self._paint_string(self.h - 2, 0, [" " * self._left_width()])
        x = int((self._left_width() - 2) / 2)
        self._paint_string(self.h - 2, x, [str(number)])

    def paint_options_menu(self):
        pass




def main(stdscr):
    # A TUI class is instaciated and given the dialogs file.
    tui = CursesTUI(stdscr, dialogs)
    if tui.width < 68:
        raise Exception('Screen width too small.')

    # Paint the main title until a key is pressed.
    tui.paint_main_title()
    stdscr.getkey()
    tui.clear()

    # Paint the main menu and get the option selected.
    o1 = tui.paint_main_menu()
    tui.clear()

    if o1 == 0:
        # Choose players in player screen.
        players = tui.paint_player_menu()
        game = TODGame(players, options['language'])

        # Randomize player order.
        game.shuffle_players()

        # Set game variables for menu options and question kind.
        exit = False
        o2 = 0
        kind = ''
        player = None

        # Begin the game.
        while not exit:
            if o2 == 0:
                # Next player:
                tui.clear()
                player = game.next_player()
                kind = tui.paint_choice_menu(player)
                tui.clear()
                tui.paint_question(game.ask_question(kind))
            elif o2 == 1:
                # Change question:
                tui.clear()
                tui.paint_question(game.ask_question(kind))
            elif o2 == 2:
                # Print random player:
                tui.paint_player_below(game.get_random_player(player))
            elif o2 == 3:
                # Print random number:
                tui.paint_random_number(game.get_random_number())
            else:
                exit = True
            o2 = tui.paint_question_menu()
    elif o1 == 1:
        tui.clear()
        back = False
        while not back:
            tui.paint_options_menu()
            back = True


curses.wrapper(main)
