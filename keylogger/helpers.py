PHRASE = "the quick brown fox jumps over the lazy dog."


def get_char_from_key_code(key_code):
    return key_code.char if str(key_code).endswith("'") else " "


def prettify(attempt, mode=None):
    resulting_string = ""
    for entry in attempt:
        if entry[2].endswith("PRESS"):
            if mode == 2:
                resulting_string += get_char_from_key_code(entry[1])
            else:
                resulting_string += entry[1][2] if entry[1].endswith("'") else " "
    return resulting_string


def attempt_is_correct(attempt, mode=None):
    return prettify(attempt, mode).casefold() == PHRASE.casefold()


def delete_special_keys(attempt):
    cleaned_attempt = []
    for entry in attempt:
        to_check = str(entry[1])
        if (
            to_check.startswith(" Key") or to_check.startswith("Key")
        ) and not to_check.endswith("space"):
            continue
        cleaned_attempt.append(entry)
    return cleaned_attempt


def update_time(attempt):
    start_time = int(attempt[0][0])
    for entry in attempt:
        new_time = int(entry[0]) - start_time
        entry[0] = new_time
    return attempt
