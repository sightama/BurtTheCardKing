""" Implementation of the windows_bot for the Eternal Card Game TCG bot application. """
from .windows_bot import WindowsBot
from .exceptions import InvalidEternalWindow
import win32gui  # pip install pywin32 to get this.


class EternalBot(WindowsBot):
    def __init__(self):
        windows_size = None
        super().__init__()
        self.origin, self.windows_size = self.normalize_to_window()

    def normalize_to_window(self):
        # Assumption: Only one Eternal client is running..
        rect = []
        win32gui.EnumWindows(output_all_windows, rect)
        x = rect[0][0]
        y = rect[0][1]
        w = rect[0][2] - x
        h = rect[0][3] - y
        if any([x, y, w, h]) < 0:  # Values cant be negative numbers. EnumWIndows is freaking out....(multi-monitor?)
            raise InvalidEternalWindow()
        return (x, y), (w, h)  # First is origin, second is size.


def output_all_windows(hwnd, extra):
    """"""
    rect = win32gui.GetWindowRect(hwnd)
    window_name = win32gui.GetWindowText(hwnd)
    if window_name == 'Eternal Card Game':
        extra.append(rect)
    #print(window_name)
