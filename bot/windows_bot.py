"""
Windows implementation of abstract bot class for GUI automation on applications such as Eternal, etc...
A lot of information sourced directly from here: https://automatetheboringstuff.com/chapter18/
for (x, y): x goes from left to right on your screen, y goes from up to down, starting at (0,0)
if u have 1920x1080 monitor, top left is (0,0), bottom right is (1919, 1079).
"""
import pyautogui
from .bot import Bot
from .exceptions import InvalidWindowsButton

pyautogui.PAUSE = 1  # Wait 1 second after each pyautogui function call.
pyautogui.FAILSAFE = True  # Move mouse as far up and left as possible to raise pyautogui.FailSafeException


class WindowsBot(Bot):
    origin = (0, 0)

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def normalize_to_window(self):
        # TODO: Display to users window screen options, then choose one and put the top left corner of it as origin.
        pass

    def mouse_move(self, position: tuple, move_time: float = 0.40):
        """ move_time = duration = time it takes to move the mouse to the new position on screen."""
        # TODO: Investigate pyautogui.moveRel (moves relative to mouses current position).
        pyautogui.moveTo(position[0], position[1], duration=move_time)

    def mouse_click(self, pos: tuple = None, mouse_button: str = 'left'):
        """
        Will click at input position using one of these mouse button options: (left|middle|right).
        Otherwise clicks where the mouse already exists at. pyautogui.doubleClick() also exists.
        """
        pyautogui.click(pos[0], pos[1], button=mouse_button) if pos else pyautogui.click(button=mouse_button)

    def mouse_drag(self, pos: tuple, move_time: float = 0.40):
        """ CLicks at existing location and drags to location and un-clicks. dragRel is also a thing. """
        pyautogui.dragTo(pos[0], pos[1], duration=move_time)

    def button_press(self, button: str):
        if button in pyautogui.KEYBOARD_KEYS:
            pyautogui.typewrite([button])
        else:
            raise InvalidWindowsButton(f'Invalid button choice supplied for pressing: {button}')

    def typewrite(self, message: str, wait_interval: float = 0.25):
        """ Type out a string. wait_interval = number of seconds between each key press. """
        pyautogui.typewrite(message=message, interval=wait_interval)

    def combination_press(self, buttons: tuple):
        """
        Press multipole key combinations together. Pulls from user-provided list,
        which contains keys from pyautogui.KEYBOARD_KEYS
        """
        # e.g. pyautogui.hotkey('ctrl', 'c'),  hotkey('ctrl', 'alt', 'shift', 's')
        pyautogui.hotkey(*buttons)
