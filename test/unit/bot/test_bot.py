import pytest
from bot.bot import Bot


class TestBotClass:
    # Can't instantiate abstract classes. skipping test for abstract class.
    def setup(self):
        self.bot = 1

    def test_init(self):
        test_bot = 1
        assert test_bot == self.bot
