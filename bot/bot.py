"""Bot implementation to mimic GUI automation workflows"""
from abc import ABC, abstractmethod


class Bot(ABC):
    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def origin(self):
        pass

    @abstractmethod
    def normalize_to_window(self):
        pass

    @abstractmethod
    def mouse_move(self):
        pass

    @abstractmethod
    def mouse_drag(self):
        pass

    @abstractmethod
    def mouse_click(self):
        pass

    @abstractmethod
    def button_press(self):
        pass

    @abstractmethod
    def typewrite(self):
        pass

    @abstractmethod
    def combination_press(self):
        pass

    # TODO: TBD
    # @abstractmethod
    # def scroll(self):
    #     pass
