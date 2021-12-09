import csv
import json
import os
import pandas as pd
import helpers


# Format of the output
# { "user": [ attempt := [ entry := [time := int, key := Key, event := str] ] ]
def transform_data_to_array():
    all_data = {}
    for folder in os.listdir("CollectedData/"):
        path = "CollectedData/" + folder + "/"
        single_data = []
        for file in os.listdir(path):
            with open(path + file) as csv_file:
                attempt = list(csv.reader(csv_file))
                attempt = helpers.delete_special_keys(attempt)
                attempt = helpers.update_time(attempt)
                if helpers.attempt_is_correct(attempt):
                    single_data.append(attempt)
        all_data[folder] = single_data
    return all_data


def get_event_array(attempt, event):
    event_keys = []
    for entry in attempt:
        if entry[2].endswith(event):
            event_keys.append(entry)
    event_diff = []
    for i in range(1, len(event_keys)):
        aft = int(event_keys[i][0])
        pre = int(event_keys[i - 1][0])
        event_diff.append(aft - pre)
    return event_diff


def get_hold_time_array(attempt, mode=None):
    hold_time_array = []
    for i in range(len(attempt) - 1):
        key_pressed = attempt[i]
        if key_pressed[2].endswith("RELEASE"):
            continue
        key_pressed_timestamp = int(key_pressed[0])
        for j in range(i + 1, len(attempt)):
            key_released = attempt[j]
            key_pressed_check = (
                key_pressed[1]
                if mode is None
                else helpers.get_char_from_key_code(key_pressed[1])
            )
            key_released_check = (
                key_released[1]
                if mode is None
                else helpers.get_char_from_key_code(key_released[1])
            )
            condition = (
                key_pressed_check.casefold() == key_released_check.casefold()
                and key_released[2].endswith("RELEASE")
            )
            if condition:
                key_released_timestamp = int(key_released[0])
                hold_time_array.append(key_released_timestamp - key_pressed_timestamp)
                break

    return hold_time_array


def get_release_press_array(data, mode=None):
    release_press_array = []
    for i in range(len(data) - 1):
        key_to_release = data[i]
        if key_to_release[2].endswith("RELEASE"):
            continue
        released_key = None
        next_pressed_key = None
        for j in range(i + 1, len(data)):
            key_to_release_ch = (
                key_to_release[1]
                if mode is None
                else helpers.get_char_from_key_code(key_to_release[1])
            )
            key_to_check_ck = (
                data[j][1]
                if mode is None
                else helpers.get_char_from_key_code(data[j][1])
            )
            if key_to_release_ch.casefold() == key_to_check_ck.casefold() and data[j][
                2
            ].endswith("RELEASE"):
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


def get_processed_data(to_file=False, file_name=None):
    raw_data = transform_data_to_array()
    data = {}
    for user_key in raw_data:
        data[user_key] = {
            "hold_time": list(),
            "press_press": list(),
            "release_press": list(),
            "release_release": list(),
            "raw_data": list(),
        }
        for collected_data in raw_data[user_key]:
            data[user_key]["press_press"].append(
                get_event_array(collected_data, "PRESS")
            )
            data[user_key]["release_release"].append(
                get_event_array(collected_data, "RELEASE")
            )
            data[user_key]["hold_time"].append(get_hold_time_array(collected_data))
            data[user_key]["release_press"].append(
                get_release_press_array(collected_data)
            )
            data[user_key]["raw_data"].append(collected_data)
        keys_pressed = list(helpers.PHRASE)
        inter_keys = [
            f"{helpers.PHRASE[i]}-{helpers.PHRASE[i + 1]}"
            for i in range(len(helpers.PHRASE) - 1)
        ]
        data[user_key]["hold_time_df"] = pd.DataFrame(
            data[user_key]["hold_time"], columns=keys_pressed
        )
        data[user_key]["press_press_df"] = pd.DataFrame(
            data[user_key]["press_press"], columns=inter_keys
        )
        data[user_key]["release_release_df"] = pd.DataFrame(
            data[user_key]["release_release"], columns=inter_keys
        )
        data[user_key]["release_press_df"] = pd.DataFrame(
            data[user_key]["release_press"], columns=inter_keys
        )

    if to_file:
        # data_to_save = {k: v for k, v in data.items() if not k.endswith('df')}
        data_to_save = {
            k_1: {k_2: v_2 for k_2, v_2 in data[k_1].items() if not k_2.endswith("df")}
            for k_1, v_1 in data.items()
        }
        with open(file_name, "w") as file:
            json.dump(data_to_save, file)
    return data


if __name__ == "__main__":
    processed_data = get_processed_data()
    total = 0
    for user in processed_data:
        print(user)
        user_total = len(processed_data[user]["raw_data"])
        print(f"\tTotal cases: {user_total}")
        total += user_total
    print(f"Total cases: {total}")
