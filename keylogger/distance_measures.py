from sklearn import metrics

from data_processer import transform_data_to_array, get_event_array, get_hold_time_array, \
    get_release_press_array_magically, get_processed_data
import pandas as pd
from sklearn.neighbors import DistanceMetric
import numpy as np


# def get_unordered_absolut_data():
#     raw_data = transform_data_to_array()
#     processed_data = {}
#     for user in raw_data:
#         if user == "Russian_or_Chinese_hacker":
#             continue
#         processed_data[user] = {
#             "hold_time": [],
#             "press_press": [],
#             "release_press": [],
#             "release_release": []
#         }
#         for collected_data in raw_data[user]:
#             processed_data[user]["press_press"].append(get_event_array(collected_data, "PRESS"))
#             processed_data[user]["release_release"].append(get_event_array(collected_data, "RELEASE"))
#             processed_data[user]["hold_time"].append(get_hold_time_array(collected_data))
#             processed_data[user]["release_press"].append(get_release_press_array_magically(collected_data))
#     return processed_data


def filter_faulty_sequences(p_data, target_chars=44):
    for user in p_data:
        for metric_type in p_data[user]:
            print("{}; {} > Original size: {}".format(user, metric_type, len(p_data[user][metric_type])))
            p_data[user][metric_type][:] = np.array([d for d in p_data[user][metric_type] if not len(d) != target_chars])
            p_data[user][metric_type] = np.array(p_data[user][metric_type])
            print("{}; {} > Cleaned size: {}".format(user, metric_type, len(p_data[user][metric_type])))
    return p_data


def produce_merged_model(p_data, user):
    model = pd.DataFrame(p_data[user]).mean().values
    return model


def produce_models(p_data, user):
    models = {}
    for metric_type in p_data[user]:
        model = pd.DataFrame(p_data[user][metric_type]).mean().values
        models[metric_type] = model
    return models


def get_distance(model, entry, distance_measure):
    dist = DistanceMetric.get_metric(distance_measure)
    dist = dist.pairwise(model.reshape(1, len(model)), entry)[0]
    return dist


def get_eer(distance_user, distance_intruder):
    # min_d = np.min(distance_user.min(), distance_intruder.min())
    # max_d = np.max(distance_user.max(), distance_intruder.max())
    # step_size = (max_d-min_d)/100
    # for step in np.arange(min_d, max_d, step_size):
    #     far = distance_user > step
    #     frr = distance_user <= step
    labels_user = np.zeros(len(distance_user))
    labels_intruder = np.ones(len(distance_intruder))
    labels = np.concatenate([labels_user, labels_intruder])
    distances = np.concatenate([distance_user, distance_intruder])

    fpr, tpr, threshold = metrics.roc_curve(y_true=labels, y_score=distances, drop_intermediate=False)
    fnr = 1 - tpr
    eer1 = fpr[np.nanargmin(np.absolute((fnr - fpr)))]
    eer2 = fnr[np.nanargmin(np.absolute((fnr - fpr)))]
    if np.absolute(eer1-eer2) > 0.01:
        print("ERROR eer1: {} and eer2: {} diverging".format(eer1, eer2))
    return eer1


def compare_disjunct(data, user="Joel"):
    models = produce_models(data, user)

    distances_user = {} # User distances by metric
    distances_intruder = {} # Intruder distances by metric
    for user_d in data:
        for metric in data[user_d]:
            if metric != "raw_data":
                distances_intruder.setdefault(metric, [])
                distance = get_distance(models[metric], data[user_d][metric], "manhattan")
                if user_d == user:
                    distances_user[metric] = distance
                else:
                    distances_intruder[metric] = np.concatenate([distances_intruder.setdefault(metric, []), distance])
                # print("{}; {}; {} > {}".format(user_m, user_d, metric, distance.mean()))
    for metric in distances_user:
        print(len(distances_user[metric]))
        print(distances_user[metric].mean())
        print(len(distances_intruder[metric]))
        print(distances_intruder[metric].mean())
        eer = get_eer(np.array(distances_user[metric]), distances_intruder[metric])
        print("User: {}; Metric: {} > EER: {}".format(user, metric, eer))


# def merge_data(p_data):
#     merged_userdata = {}
#     for user in p_data:
#         merged_metrics = []
#         for i, d in enumerate(p_data[user]["hold_time"]):
#             unified = np.concatenate([p_data[user]["hold_time"][i], p_data[user]["press_press"][i], p_data[user]["release_press"][i], p_data[user]["release_release"][i]])
#             merged_metrics.append(unified)
#         merged_userdata[user] = np.array(merged_metrics)
#     return merged_userdata


def compare_unified(data_unmerged, user="Joel"):
    data, _ = merge_data_with_split(data_unmerged)
    model = produce_merged_model(data, user)

    distances_intruder = []
    for user_d in data:
        distance = get_distance(model, data[user_d], "manhattan")
        if user_d == user:
            distances_user = distance
        else:
            distances_intruder = np.concatenate([distances_intruder, distance])
        # print("{}; {}; {} > {}".format(user_m, user_d, metric, distance.mean()))
    print(len(distances_user))
    print(distances_user.mean())
    print(len(distances_intruder))
    print(distances_intruder.mean())
    eer = get_eer(np.array(distances_user), distances_intruder)
    print("User: {}; Metric: {} > EER: {}".format(user, "Merged", eer))


def merge_data_with_split(p_data, split_off=0, random_split=False):
    merged_userdata = {}
    for user in p_data:
        merged_metrics = []
        for i, d in enumerate(p_data[user]["hold_time"]):
            unified = np.concatenate([p_data[user]["hold_time"][i], p_data[user]["press_press"][i], p_data[user]["release_press"][i], p_data[user]["release_release"][i]])
            merged_metrics.append(unified)
        merged_userdata[user] = np.array(merged_metrics)
    merged_unknown_userdata = {}
    for user in merged_userdata:
        o_size = len(merged_userdata[user])
        merged_unknown_userdata[user] = merged_userdata[user][:split_off]
        merged_userdata[user] = merged_userdata[user][split_off:]
        if o_size != len(merged_unknown_userdata[user]) + len(merged_userdata[user]):
            print("ERROR: Splitting merged data resulted in length mismatch > Check dimensions of used data")
    return merged_userdata, merged_unknown_userdata


def get_user(data_unmerged):
    data = merge_data_with_split(data_unmerged, split_off=5)

    models = {
        "Joel": produce_merged_model(data, "Joel"),
        "Alan": produce_merged_model(data, "Alan"),
        "Giancarlo": produce_merged_model(data, "Giancarlo"),
        "Natasha": produce_merged_model(data, "Natasha")
    }


if __name__ == '__main__':
    p_data = get_processed_data()
    compare_unified(p_data)

    #get_user(p_data)
    print("Finished")
