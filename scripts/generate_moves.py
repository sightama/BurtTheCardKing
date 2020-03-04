from bot.eternal_bot import EternalBot
import operator
import pyautogui
import pickle
import os.path


def delete_pos(filename, pos_names):
    with open(filename, 'rb') as fp:
        screen_positions = pickle.load(fp)
    del screen_positions[pos_names]
    with open(filename, 'wb') as fp:
        pickle.dump(screen_positions, fp, protocol=pickle.HIGHEST_PROTOCOL)


def modify_name(filename, pos_name):
    with open(filename, 'rb') as fp:
        screen_positions = pickle.load(fp)
    for x in pos_name:
        screen_positions['odd-' + x] = screen_positions.pop(x)
    with open(filename, 'wb') as fp:
        pickle.dump(screen_positions, fp, protocol=pickle.HIGHEST_PROTOCOL)


def generate_moves(filename):
    # Import existing moves.
    if os.path.isfile(filename):
        with open(filename, 'rb') as fp:
            screen_positions = pickle.load(fp)
    else:
        screen_positions = {}
    while True:
        # Have if checks for screenshots and pixel colors? (end turn button,

        eternal_bot = EternalBot()
        real_position = pyautogui.position()  # Put breakpt here and put mouse over button/move.
        rel_location = tuple(map(operator.sub, real_position, eternal_bot.origin))
        # rel_location = real_position - eternal_bot.origin
        name_of_pos = input(f"Name of created position at {real_position}: ")
        if name_of_pos == 'exit':
            break
        screen_positions[name_of_pos] = rel_location

    with open(filename, 'wb') as fp:
        pickle.dump(screen_positions, fp, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    positions = 'play/eternal/positions.p'
    generate_moves(positions)
    # delete_pos(positions, 'xit')
    # modify_name(positions, ['friendly-0', 'friendly--1', 'friendly-1', 'friendly-2', 'friendly--2'])
