""" Integration test to do end-to-end test of EternalBot for application. """
import pytest
from bot.eternal_bot import EternalBot


class TestEternalBot:
    def setup(self):
        self.eternal_bot = EternalBot()

    def test_init(self, mocker):
        assert self.eternal_bot.origin == (0, 0)
        #mocker.patch.object()


# TODO: NEXT, get the coordinates above, move the game, get them again, see if you can replicate a mouse click
# TODO; To a same location. (BURT-1)
