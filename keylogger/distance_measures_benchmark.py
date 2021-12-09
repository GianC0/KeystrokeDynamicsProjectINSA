import pandas as pd
import scipy
import numpy as np
from sklearn.neighbors import DistanceMetric
from sklearn import neighbors
from sklearn import metrics
from pathlib import Path

data_file = Path("BenchmarkData/DSL-StrongPasswordData.csv")

if __name__ == '__main__':
    df_data = pd.read_csv(data_file)
    print(df_data)
    subjects = df_data["subject"].unique()
    s_dists = []
    i_dists = []
    for s in subjects:
        s_data = df_data[df_data["subject"] == s]
        i_data = df_data[~(df_data["subject"] == s)]
        train_data = s_data[s_data["sessionIndex"] <= 4].drop(["subject", "sessionIndex", "rep"], axis=1)
        test_s_data = s_data[s_data["sessionIndex"] > 4].drop(["subject", "sessionIndex", "rep"], axis=1)
        test_i_data = i_data[(i_data["sessionIndex"] == 1) & (i_data["rep"] <= 5)].drop(["subject", "sessionIndex", "rep"], axis=1)
        dist = DistanceMetric.get_metric('euclidean')
        # cov = train_data.cov()
        # dist = DistanceMetric.get_metric('mahalanobis', VI=cov)

        model = train_data.mean().to_frame().transpose()
        s_dist = dist.pairwise(model, test_s_data)[0]
        i_dist = dist.pairwise(model, test_i_data)[0]
        s_dists.extend(s_dist)
        i_dists.extend(i_dist)
    s_dists = np.array(s_dists)
    i_dists = np.array(i_dists)
    print("Mean user distance: {}".format(np.nanmean(s_dists)))
    print("Mean intruder distance: {}".format(np.nanmean(i_dists)))
    print("Variance user distance: {}".format(np.nanvar(s_dists)))
    print("Variance intruder distance: {}".format(np.nanvar(i_dists)))
    # print(len(s_dists))
    # print(len(i_dists))

    labels_user = np.zeros(len(s_dists))
    labels_intruder = np.ones(len(i_dists))
    labels = np.concatenate([labels_user, labels_intruder])
    distances = np.concatenate([s_dists, i_dists])

    fpr, tpr, threshold = metrics.roc_curve(y_true=labels, y_score=distances)
    fnr = 1 - tpr

    eer1 = fpr[np.nanargmin(np.absolute((fnr - fpr)))]
    eer2 = fnr[np.nanargmin(np.absolute((fnr - fpr)))]
    if eer1 == eer2:
        print("ERROR: eer isn't granular enough")
    print("Equal Error Rate: {}".format(eer1))
