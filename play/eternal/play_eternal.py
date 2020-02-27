import pickle
import os.path
from bot.eternal_bot import EternalBot
from play.eternal.exceptions import InvalidPositionFile
import time


def play(pos_file):
    # Import existing moves.
    if os.path.isfile(pos_file):
        with open(pos_file, 'rb') as fp:
            positions = pickle.load(fp)
    else:
        raise InvalidPositionFile("Can't locate the position file! Please generate one with"
                                  " scripts/generate_positions.py")

    time.sleep(10)
    # Play against puzzle killer - level 2.
    bot = EternalBot()
    bot.play_card('odd-position-0', 'field-right')
    bot.play_card('even-position--1', 'field-left')
    bot.play_card('odd-position--1', 'field-left')
    bot.play_card('even-position-1', 'field-right-2')


if __name__ == '__main__':
    play('play/eternal/positions.p')
