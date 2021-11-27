from sklearn import metrics

from data_processer import transform_data_to_array, get_event_array, get_hold_time_array, \
    get_release_press_array_magically, get_processed_data
import pandas as pd
from sklearn.neighbors import DistanceMetric
import numpy as np
import random


def produce_merged_model(data, user):
    if len(data[user]) == 0:
        print("ERROR: model data is empty > Results are wrong") #Todo: Handle
    model = pd.DataFrame(data[user]).mean().values
    return model


def produce_models(data, user):
    models = {}
    for metric_type in data[user]:
        model = pd.DataFrame(data[user][metric_type]).mean().values
        models[metric_type] = model
    return models


def get_distance(model, entry, d_measure):
    dist = DistanceMetric.get_metric(d_measure)
    dist = dist.pairwise(model.reshape(1, len(model)), entry)[0]
    return dist


def get_eer(distance_user, distance_intruder):
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


def merge_data_with_split(data, split_off=0, random_split=False, metrics_tu=None):
    if metrics_tu is None:
        metrics_tu = ['hold_time', 'press_press', 'release_press', 'release_release']
    merged_userdata = {}
    for user in data:
        merged_metrics = []
        for m_tu in metrics_tu:
            if not merged_metrics:
                merged_metrics = data[user][m_tu]
            else:
                merged_metrics = list(map(np.concatenate, zip(merged_metrics, data[user][m_tu])))
        if random_split:
            random.shuffle(merged_metrics)
        merged_userdata[user] = np.array(merged_metrics)
    merged_testdata = {}
    for user in merged_userdata:
        o_size = len(merged_userdata[user])
        merged_testdata[user] = merged_userdata[user][:split_off]
        merged_userdata[user] = merged_userdata[user][split_off:]
        if o_size != len(merged_testdata[user]) + len(merged_userdata[user]):
            print("ERROR: Splitting merged data resulted in length mismatch > Check dimensions of used data")
    return merged_userdata, merged_testdata


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


def estimate_single_user(models, entry, d_measure):
    distances = {}
    for user in models:
        distances[user] = get_distance(models[user], entry.reshape(1, len(entry)), d_measure)
    determined_user, min_distance = min(distances.items(), key=lambda dist: dist[1])
    print(min_distance)
    return determined_user


def get_user(data_unmerged, split_off, random_split, metrics_tu, d_measure):
    model_data, test_data = merge_data_with_split(data_unmerged, split_off, random_split, metrics_tu)

    models = {}
    correct_est = 0
    false_est = 0
    for user in model_data:
        models[user] = produce_merged_model(model_data, user)

    for user in test_data:
        for entry in test_data[user]:
            est_user = estimate_single_user(models, entry, d_measure)
            if est_user == user:
                correct_est += 1
            else:
                false_est += 1
    print(correct_est)
    print(false_est)


# Method to use for online keylogging
# Input: - One keylogged line corresponding to 'The quick brown fox jumps over the lazy dog.'
# - The username of the tipper
def get_user_online():
    data = get_processed_data()
    data.pop("Russian_or_Chinese_hacker")


if __name__ == '__main__':
    # Parameters
    to_run = "offline_user_detection"
    on_model = "Joel"  # Only necessary for compare unified/disjunct
    nmbr_test_data = 10
    random_test_sampling = True
    metrics_to_use = ['hold_time']
    distance_measure = "manhattan"  # 'manhattan' or 'euclidean'

    # Data
    u_data = get_processed_data()
    u_data.pop("Russian_or_Chinese_hacker")

    # Analysis
    if to_run == "unified":
        compare_unified(u_data, on_model)
    elif to_run == "disjunct":
        compare_disjunct(u_data, on_model)
    elif to_run == "offline_user_detection":
        get_user(u_data, nmbr_test_data, random_test_sampling, metrics_to_use, distance_measure)

    print("Finished")

# TODO: Determine possible distance threshold for outsider class
# TODO: Make compare unified realistic
# TODO: Move prints to main method

# TODO: Produce some kind of plot
