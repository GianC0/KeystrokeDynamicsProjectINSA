from sklearn import metrics

from data_processer import transform_data_to_array, get_event_array, get_hold_time_array, \
    get_release_press_array_magically
import pandas as pd
from sklearn.neighbors import DistanceMetric
import numpy as np


def x():
    pass


def get_unordered_absolut_data():
    raw_data = transform_data_to_array()
    processed_data = {}
    for user in raw_data:
        if user == "Russian_or_Chinese_hacker":
            continue
        processed_data[user] = {
            "hold_time": [],
            "press_press": [],
            "release_press": [],
            "release_release": []
        }
        for collected_data in raw_data[user]:
            processed_data[user]["press_press"].append(get_event_array(collected_data, "PRESS"))
            processed_data[user]["release_release"].append(get_event_array(collected_data, "RELEASE"))
            processed_data[user]["hold_time"].append(get_hold_time_array(collected_data))
            processed_data[user]["release_press"].append(get_release_press_array_magically(collected_data))
    return processed_data


def filter_faulty_sequences(p_data, target_chars=44):
    for user in p_data:
        for metric_type in p_data[user]:
            print("{}; {} > Original size: {}".format(user, metric_type, len(p_data[user][metric_type])))
            p_data[user][metric_type][:] = np.array([d for d in p_data[user][metric_type] if not len(d) != target_chars])
            p_data[user][metric_type] = np.array(p_data[user][metric_type])
            print("{}; {} > Cleaned size: {}".format(user, metric_type, len(p_data[user][metric_type])))
    return p_data


def produce_models(p_data):
    models = {}
    for user in p_data:
        for metric_type in p_data[user]:
            model = pd.DataFrame(p_data[user][metric_type]).mean().values
            models[user] = model
    return models


def get_distance(model, entry, distance_measure):
    dist = DistanceMetric.get_metric(distance_measure)
    dist = dist.pairwise(model.reshape(1, 44), entry)[0]
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

    fpr, tpr, threshold = metrics.roc_curve(y_true=labels, y_score=distances)
    fnr = 1 - tpr
    eer1 = fpr[np.nanargmin(np.absolute((fnr - fpr)))]
    eer2 = fnr[np.nanargmin(np.absolute((fnr - fpr)))]
    if np.absolute(eer1-eer2) > 0.01:
        print("ERROR eer1: {} and eer2: {} diverging".format(eer1, eer2))
    return eer1


if __name__ == '__main__':
    processed_data = get_unordered_absolut_data()

    filtered_data = filter_faulty_sequences(processed_data)

    models = produce_models(processed_data)

    results = {}
    for user_m in models:
        results[user_m] = {}
        model = models[user_m]
        for user_d in filtered_data:
            results[user_m][user_d] = {}
            for metric in filtered_data[user_d]:
                data = filtered_data[user_d][metric]
                distance = get_distance(model, data, "manhattan")
                results[user_m][user_d][metric] = distance
                # print("{}; {}; {} > {}".format(user_m, user_d, metric, distance.mean()))

    distances_intruder = {}
    distances_user = {}
    for user_m in results:
        distances_intruder[user_m] = {}
        distances_user[user_m] = {}
        for user_d in results[user_m]:
            for metric in results[user_m][user_d]:
                distances_intruder[user_m].setdefault(metric, [])
                if user_m == user_d:
                    distances_user[user_m][metric] = results[user_m][user_d][metric]
                else:
                    distances_intruder[user_m][metric].append(results[user_m][user_d][metric])
    for user in distances_user:
        for metric in distances_user[user]:
            eer = get_eer(np.array(distances_user[user][metric]), np.concatenate(distances_intruder[user][metric]))
            print("User: {}; Metric: {} > EER: {}".format(user, metric, eer))
    print("Finished")
