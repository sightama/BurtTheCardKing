import pytest
from bot.eternal_bot import EternalBot


class TestEternalBot:
    def setup(self):
        self.eternal_bot = EternalBot()

    def test_init(self, mocker):
        assert self.eternal_bot.origin == (0, 0)
        #mocker.patch.object()
