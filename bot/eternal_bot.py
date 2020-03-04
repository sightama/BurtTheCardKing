""" Implementation of the windows_bot for the Eternal Card Game TCG bot application. """
from .windows_bot import WindowsBot
from .exceptions import InvalidEternalWindow, NoEternalWindowError
import win32gui  # pip install pywin32 to get this.
import operator
import pickle

with open('play/eternal/positions.p', 'rb') as fp:
    POSITIONS = pickle.load(fp)


class EternalBot(WindowsBot):
    def __init__(self):
        windows_size = None

        super().__init__()
        self.origin, self.windows_size = self.normalize_to_window()

    def normalize_to_window(self):
        # Assumption: Only one Eternal client is running..
        rect = []
        win32gui.EnumWindows(output_all_windows, rect)
        if not rect:  # Eternal window not open
            raise NoEternalWindowError('Please instantiate the Eternal window by booting the game from steam.')
        x = rect[0][0]
        y = rect[0][1]
        w = rect[0][2] - x
        h = rect[0][3] - y
        if any(i < 0 for i in [x, y, w, h]):
            raise InvalidEternalWindow('Error acquiring window (win32gui bug); Focus eternal window & try again.')
        return (x, y), (w, h)  # First is origin, second is size.

    def play_card(self, game_pos, side):
        """
        Allows you to play a card from hand. Reference POSITIONS for pos optionional params. side is which
        side of field to throw the card onto.
        """
        # Select and move over the card position.
        card_pos = tuple(map(operator.add, self.origin, POSITIONS[game_pos]))
        self.mouse_move(card_pos)
        field_side = tuple(map(operator.add, self.origin, POSITIONS[side]))
        self.mouse_drag(field_side)


def output_all_windows(hwnd, extra):
    coordinates = win32gui.GetWindowRect(hwnd)
    window_name = win32gui.GetWindowText(hwnd)
    if window_name == 'Eternal Card Game':
        extra.append(coordinates)
