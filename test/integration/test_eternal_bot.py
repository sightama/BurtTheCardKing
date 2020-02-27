""" Integration test to do end-to-end test of EternalBot for application. """
import pytest
from bot.eternal_bot import EternalBot
import operator


# mocker.patch.object()

class TestEternalBot:
    def setup(self):
        self.eternal_bot = EternalBot()

    def test_init(self, mocker):
        assert self.eternal_bot.origin != (0, 0)
        # mocker.patch.object()

    def test_mouse_simple_transformation(self):
        # Use already existing instance.
        self.eternal_bot.mouse_click(self.eternal_bot.origin)
        assert 1
        self.eternal_bot = EternalBot()
        self.eternal_bot.mouse_click(self.eternal_bot.origin)
        assert True

    @pytest.mark.lane
    def test_mouse_simple_transformation(self):
        # Use already existing instance.
        # rel_location = real_position - self.eternal_bot.origin
        rel_golden_dot = (966, 453)
        golden_dot = tuple(map(operator.add, self.eternal_bot.origin, rel_golden_dot))
        self.eternal_bot.mouse_click(golden_dot)
        assert 1
        self.eternal_bot = EternalBot()
        self.eternal_bot.mouse_click(self.eternal_bot.origin)
        assert True

