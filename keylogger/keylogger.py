from pynput.keyboard import Listener
from pynput import keyboard
import logging
import time
from datetime import datetime
import sys
import data_processer
import distance_measures
import numpy as np

mode = 0 # undefined mode
data = []
array_of_single_line = []
line = 1
logger = None


# The quick brown fox jumps over the lazy dog.
def on_press(key):
    global data, array_of_single_line
    if key == keyboard.Key.esc:
        return False
    if key == keyboard.Key.enter:
        if mode == 2:
            return False
        data.append(array_of_single_line.copy())
        array_of_single_line.clear()
    else:
        timestamp = int(round(time.time() * 1000))
        action = "PRESS"
        array_of_single_line.append([timestamp, key, action])
        # print(dynamic_array)
    # logging.info(str(int(round(time.time() * 1000))) + " PRESS " + str(key))


def on_release(key):
    global line
    if key == keyboard.Key.enter:
        if mode == 2:
            return False
        print(f"\n{line}", end=" ")
        line += 1
    else:
        timestamp = int(round(time.time() * 1000))
        action = "RELEASE"
        array_of_single_line.append([timestamp, key, action])
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
print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿         CHOOSE MODE         ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
print("⣿ 1 - Collect more data                           ⣿⣿⣿⣿")
print("⣿ 2 - Test our amazing user detection algorithm   ⣿⣿⣿⣿")
print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")

mode = int(input())
while not mode in range(1, 3):
    mode = int(input())
    print("⣿ Pleas only use a mode from the list :( ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")

if mode == 1:
    # Here we collect new data
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

    nr = 0
    while not nr in range(1, 6):
        nr = input()
        print("⣿ Pleas only use a pokemon from the list :( ⣿⣿⣿⣿")

    pokemons = ["Alan", "Natasha", "Joel", "Giancarlo", "Russian_or_Chinese_hacker"]

    pokemon = pokemons[int(nr) - 1]
    log_dir = "CollectedData/" + pokemon + "/"
    temp_dir = "Temp/"

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
else:
    # Here is where we determine the user
    password_correct = False
    while not password_correct:
        array_of_single_line.clear()
        time.sleep(1)
        print("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ Please type in the password ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n")
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        cleaned_data = data_processer.delete_special_keys(array_of_single_line)
        password_correct = data_processer.item_is_correct(cleaned_data, mode=mode)

    cleaned_time = data_processer.update_time(cleaned_data)
    hold_time = data_processer.get_hold_time_array(cleaned_time, mode=mode)
    press_press = data_processer.get_event_array(cleaned_time, "PRESS")
    release_release = data_processer.get_event_array(cleaned_time, "RELEASE")
    release_press = data_processer.get_release_press_array_magically(cleaned_time, mode=mode)

    # This is the entry, but it doesn't work. It worked just with  distance_measures.get_user_online(np.asarray(hold_time)) though
    user_to_check = {
        "user_to_check": {
            "hold_time": hold_time,
            "press_press": press_press,
            "release_release": release_release,
            "release_press": release_press
        }
    }

    result = distance_measures.get_user_online(user_to_check, metrics_tu=['hold_time','press_press','release_release','release_press'])
    # result = distance_measures.get_user_online(np.asarray(hold_time))

    print(result)

# TODO: just start the keylogger class and choose the mode 2, then type the passwors