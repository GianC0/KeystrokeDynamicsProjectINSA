from pynput.keyboard import Listener
from pynput import keyboard
import logging
import time
from datetime import datetime

data = []

def on_press(key):
    if key == keyboard.Key.esc:
        return False
    timestamp = int(round(time.time() * 1000))
    action = "PRESS"
    data.append([timestamp, key, action])
    # logging.info(str(int(round(time.time() * 1000))) + " PRESS " + str(key))

def on_release(key):
    timestamp = int(round(time.time() * 1000))
    action = "RELEASE"
    data.append([timestamp, key, action])
    # logging.info(str(int(round(time.time() * 1000))) + " RELEASE " + str(key))


print("########################################################")
print("##########      CHOOSE YOUR POKEMON         ############")
print("########################################################")
print("# 1 - Alan                                  ############")
print("# 2 - Natasha                               ############")
print("# 3 - Joel                                  ############")
print("# 4 - Giancarlo                             ############")
print("# 5 - Marcus                                ############")
print("# 5 - Anonymous hacker                      ############")
print("""########################################################
##########   `;-.          ___,         ################   
##########     `.`\_...._/`.-"`         ################
##########       \        /      ,          ############
##########       /()   () \    .' `-._          ########
##########      |)  .    ()\  /   _.'           ########
##########      \  -'-     ,; '. <          ############
##########       ;.__     ,;|   >           ############         
##########      / ,    / ,  |.-'.-'         ############         
##########     (_/    (_/ ,;|.<`            ############         
##########       \    ,     ;-`         ################
##########        >   \    /            ################
##########       (_,-'`> .'         ####################         
##########           (_,'           ####################         
########################################################""")


nr = input()

pokemons = ["Alan", "Natasha", "Joel", "Giancarlo", "Marcus", "Russian_or_Chinese_hacker"]

pokemon = pokemons[int(nr) - 1]
log_dir = "CollectedData/" + pokemon + "/"
log_timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mm%Ss")
logging.basicConfig(filename=(log_dir + log_timestamp + ".csv"), level=logging.DEBUG, format='%(message)s')


with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()

start_timestamp = data[0][0]

for item in data:
    item[0] -= start_timestamp
    # log = [str(item[0]), str(item[1]), item[2]]
    logging.info(str(item[0]) + ', ' + str(item[1]) + ', ' + item[2])
