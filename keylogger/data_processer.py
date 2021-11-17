import csv
import os

def pretty_case(item):
    resulting_string = ""
    for event in item:
        if event[2].endswith("PRESS"):
            resulting_string += event[1][2] if event[1].endswith("'") else " "
    return resulting_string

def item_is_correct(item):
    return pretty_case(item).casefold() == "the quick brown fox jumps over the lazy dog.".casefold()


def delete_special_keys(item):
    new_item = []
    for event in item:
        if event[1].startswith(" Key") and not event[1].endswith("space"):
            continue
        new_item.append(event)
    return new_item

def update_time(item):
    start_time = int(item[0][0])
    for event in item:
        new_time = int(event[0]) - start_time
        event[0] = new_time
    return item

def transform_data_to_array():
    all_data = {}
    for folder in os.listdir("CollectedData/"):
        path = "CollectedData/" + folder + "/"
        pokemon_data = []
        for file in os.listdir(path):
            with open(path + file) as csvfile:
                pokemon_item = list(csv.reader(csvfile))
                pokemon_item = delete_special_keys(pokemon_item)
                pokemon_item = update_time(pokemon_item)
                if item_is_correct(pokemon_item):
                    pokemon_data.append(pokemon_item)
        all_data[folder] = pokemon_data
    return all_data  # Format: {user: collected_data}, collected_data: [experiment], experiment: [data_sample], data_sample: [timestamp, character, action]


def get_event_array(data, event):
    press_pres_keys = []
    for key_info in data:
        if key_info[2].endswith(event):
            press_pres_keys.append(key_info)
    press_press_diff = []
    for i in range(1, len(press_pres_keys)):
        aft = int(press_pres_keys[i][0])
        pre = int(press_pres_keys[i - 1][0])
        press_press_diff.append(aft - pre)

    return press_press_diff


def get_hold_time_array(data):
    hold_time_array = []
    for i in range(len(data) - 1):
        key_pressed = data[i]
        if key_pressed[2].endswith("RELEASE"):
            continue
        key_pressed_timestamp = int(key_pressed[0])
        for j in range(i + 1, len(data)):
            key_released = data[j]
            if key_pressed[1].casefold() == key_released[1].casefold() and key_released[2].endswith("RELEASE"):
                key_released_timestamp = int(key_released[0])
                hold_time_array.append(key_released_timestamp - key_pressed_timestamp)
                break

    return hold_time_array


def get_release_press_array_magically(data):
    release_press_array = []
    for i in range(len(data) - 1):
        key_to_release = data[i]
        if key_to_release[2].endswith("RELEASE"):
            continue
        for j in range(i+1, len(data)):
            if key_to_release[1].casefold() == data[j][1].casefold() and data[j][2].endswith("RELEASE"):
                released_key = data[j]
                break
        char_found = False
        for j in range(i + 1, len(data)):
            if data[j][2].endswith("PRESS"):
                next_pressed_key = data[j]
                char_found = True
                break
        if char_found:
            released_timestamp = int(released_key[0])
            pressed_timestamp = int(next_pressed_key[0])
            release_press_array.append(pressed_timestamp - released_timestamp)

    return release_press_array


def count_backspace(data):
    count = 0
    for i in range(len(data)):
        if data[i][1].endswith("Key.backspace") and data[i][2].endswith("PRESS"):
            count += 1
    return count

def get_processed_data():
    raw_data = transform_data_to_array()
    processed_data = {}
    for user in raw_data:
        processed_data[user] = {
            "hold_time": [],
            "press_press": [],
            "release_press": [],
            "release_release": [],
            "raw_data": []
        }
        for collected_data in raw_data[user]:
            processed_data[user]["press_press"].append(get_event_array(collected_data, "PRESS"))
            processed_data[user]["release_release"].append(get_event_array(collected_data, "RELEASE"))
            processed_data[user]["hold_time"].append(get_hold_time_array(collected_data))
            processed_data[user]["release_press"].append(get_release_press_array_magically(collected_data))
            processed_data[user]["raw_data"].append(collected_data)
    return processed_data


if __name__ == "__main__":
    processed_data = get_processed_data()
    total = 0
    for user in processed_data:
        user_total = 0
        print(user)
        for item in processed_data[user]:
            print(f"\t{item}:", end=" ")
            for case in processed_data[user][item]:
                print(len(case), end=", ")
            print("\b\b")
        user_total = len(processed_data[user]["raw_data"])
        print(f"\tTotal cases: {user_total}")
        total += user_total
    print(f"Total cases: {total}")
