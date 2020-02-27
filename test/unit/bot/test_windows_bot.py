import pytest
from bot.windows_bot import WindowsBot


class TestWindowsBot:
    def setup(self):
        self.bot = WindowsBot()

    def test_init(self):
        assert self.bot.origin == (0, 0)
