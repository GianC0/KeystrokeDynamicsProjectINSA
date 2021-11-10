from pynput.keyboard import Listener
from pynput import keyboard
import logging
import time
from datetime import datetime
import sys

data = []
dynamic_array = []
line = 1
logger = None

# The quick brown fox jumps over the lazy dog.
def on_press(key):
    global data, dynamic_array
    if key == keyboard.Key.esc:
        return False
    if key == keyboard.Key.enter:
        data.append(dynamic_array.copy())
        dynamic_array.clear()
    else:
        timestamp = int(round(time.time() * 1000))
        action = "PRESS"
        dynamic_array.append([timestamp, key, action])
        # print(dynamic_array)
    # logging.info(str(int(round(time.time() * 1000))) + " PRESS " + str(key))


def on_release(key):
    global line
    if key == keyboard.Key.enter:
        print(f"\n{line}", end=" ")
        line += 1
    else:
        timestamp = int(round(time.time() * 1000))
        action = "RELEASE"
        dynamic_array.append([timestamp, key, action])
        # print(dynamic_array)
    # logging.info(str(int(round(time.time() * 1000))) + " RELEASE " + str(key))


def initLogging(filename):
    global logger
    if logger is None:
        logger = logging.getLogger()
    else:  # wish there was a logger.close()
        for handler in logger.handlers[:]:  # make a copy of the list
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(message)s')

    fh = logging.FileHandler(filename)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)


print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿      CHOOSE YOUR POKEMON         ⣿⣿⣿⣿⣿⣿⣿")
print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("⣿ 1 - Alan                                  ⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("⣿ 2 - Natasha                               ⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("⣿ 3 - Joel                                  ⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("⣿ 4 - Giancarlo                             ⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("⣿ 5 - Russian or Chinese hacker             ⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("""⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿""")
print()

nr = input()

pokemons = ["Alan", "Natasha", "Joel", "Giancarlo", "Russian_or_Chinese_hacker"]

pokemon = pokemons[int(nr) - 1]
log_dir = "CollectedData/" + pokemon + "/"


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

i = 0
for array in data:
    log_timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mm%Ss")
    initLogging(log_dir + log_timestamp + str(i) + ".csv")
    i += 1
    start_timestamp = array[0][0]
    for item in array:
        item[0] -= start_timestamp
        # log = [str(item[0]), str(item[1]), item[2]]
        logging.info(str(item[0]) + ', ' + str(item[1]) + ', ' + item[2])

