import pickle
import os.path
from bot.eternal_bot import EternalBot
from play.eternal.exceptions import InvalidPositionFile
import time


def play_random(pos_file):
    time.sleep(10)
    # Play against puzzle killer - level 2.
    bot = EternalBot()
    bot.play_card('odd-position-0', 'field-right')
    bot.play_card('even-position--1', 'field-left')
    bot.play_card('odd-position--1', 'field-left')
    bot.play_card('even-position-1', 'field-right-2')


def play_simple(pos_file):
    time.sleep(10)
    # Play against puzzle killer - level 2.
    bot = EternalBot()
    bot.play_card('odd-position-0', 'field-right')
    bot.play_card('even-position--1', 'field-left')
    bot.play_card('odd-position--1', 'field-left')
    bot.play_card('even-position-1', 'field-right-2')


def load_pickle(pos_file):
    # Import existing moves.
    if os.path.isfile(pos_file):
        with open(pos_file, 'rb') as fp:
            positions = pickle.load(fp)
    else:
        raise InvalidPositionFile("Can't locate the position file! Please generate one with"
                                  " scripts/generate_positions.py")
    return positions


if __name__ == '__main__':
    try:
        moves = load_pickle('play/eternal/positions.p')
        print(moves)
        # play_random()
        play_simple()
    except Exception as ex:
        raise ex
