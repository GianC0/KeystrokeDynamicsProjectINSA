import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score


INTRUDER_USERNAME = "intruders"
PHRASE = ["period", "t", "i", "e", "five", "Shift.r", "o", "a", "n", "l", "Return"]
sns.set()
mpl.rcParams["figure.figsize"] = (15, 10)


def get_press_time_of_key(attempt, key_index):
    press_count = 0
    for entry in attempt:
        if entry[2].endswith("PRESS"):
            if press_count == key_index:
                return entry[0]
            press_count += 1
    return None


def convert_dict_to_pandas(data):
    l_data = []
    _id = 0
    i = 0
    for user in data:
        attempts_made = len(data[user]["raw_data"])
        for attempt in range(attempts_made):
            l_data.append(
                [
                    _id,
                    0,
                    user,
                    0,
                    data[user]["hold_time"][attempt][0],
                    np.NaN,
                    np.NaN,
                ]
            )
            i += 1
            for key in range(1, 44):
                press_time = get_press_time_of_key(data[user]["raw_data"][attempt], key)
                hold_time = data[user]["hold_time"][attempt][key]
                release_press_time = data[user]["release_press"][attempt][key - 1]
                press_press_time = data[user]["press_press"][attempt][key - 1]
                l_data.append(
                    [
                        _id,
                        key,
                        user,
                        press_time,
                        hold_time,
                        release_press_time,
                        press_press_time,
                    ]
                )
            _id += 1
    return pd.DataFrame(
        l_data,
        columns=[
            "id",
            "key_no",
            "user",
            "PT",
            "HT",
            "RPT",
            "PPT",
        ],
    ).set_index(["id", "key_no"])


def bucket_dataframe(_df):
    no_of_bins = 10

    ht_max = _df["HT"].max()
    rpt_max = _df["RPT"].max()
    ppt_max = _df["PPT"].max()

    labels = [i for i in range(no_of_bins)]

    new_df = _df.copy()

    new_df["HTEnc"], ht_bins = pd.qcut(
        new_df["HT"], retbins=True, labels=labels, q=no_of_bins
    )
    new_df["PPTEnc"], rpt_bins = pd.qcut(
        new_df["PPT"], retbins=True, labels=labels, q=no_of_bins
    )
    new_df["RPTEnc"], ppt_bins = pd.qcut(
        new_df["RPT"], retbins=True, labels=labels, q=no_of_bins
    )

    new_df["HTEnc"] = new_df["HTEnc"].astype(str).replace("nan", -1).astype(int)
    new_df["PPTEnc"] = new_df["PPTEnc"].astype(str).replace("nan", -1).astype(float)
    new_df["RPTEnc"] = new_df["RPTEnc"].astype(str).replace("nan", -1).astype(float)

    return new_df


def convert_to_train(_df):
    train_df_ht_temp = (
        _df.reset_index().groupby(["user", "id"])["HTEnc"].apply(np.array)
    )
    train_df_ppt_temp = (
        _df.reset_index().groupby(["user", "id"])["PPTEnc"].apply(np.array)
    )
    train_df_rpt_temp = (
        _df.reset_index().groupby(["user", "id"])["RPTEnc"].apply(np.array)
    )

    train_df_user_all_sample_props = pd.DataFrame(
        {
            "HT": train_df_ht_temp,
            "PPT": train_df_ppt_temp,
            "RPT": train_df_rpt_temp,
        }
    )

    train_df_user_all_sample_props = (
        pd.DataFrame(
            train_df_user_all_sample_props.HT.tolist(),
            index=train_df_user_all_sample_props.index,
        )
        .add_prefix("HT_")
        .join(
            pd.DataFrame(
                train_df_user_all_sample_props.PPT.tolist(),
                index=train_df_user_all_sample_props.index,
            ).add_prefix("PPT_")
        )
        .join(
            pd.DataFrame(
                train_df_user_all_sample_props.RPT.tolist(),
                index=train_df_user_all_sample_props.index,
            ).add_prefix("RPT_")
        )
        .reset_index()
        .set_index("user")
        .drop(columns=["id"])
    )

    return train_df_user_all_sample_props


def get_test_dataset():
    _df = (
        pd.read_csv("knn_dataset.csv")
        .drop(columns=["sessionIndex", "rep"])
        .rename({"subject": "user"}, axis=1)
        .set_index("user")
    )
    _df["PPT_0"] = -1.0
    _df["RPT_0"] = -1.0
    new_h_names = {f"H.{value}": f"HT_{i}" for i, value in enumerate(PHRASE)}
    new_dd_names = {f"DD.{PHRASE[i - 1]}.{PHRASE[i]}": f"PPT_{i}" for i in range(1, len(PHRASE))}
    new_ud_names = {f"UD.{PHRASE[i - 1]}.{PHRASE[i]}": f"RPT_{i}" for i in range(1, len(PHRASE))}
    new_names = new_h_names | new_dd_names | new_ud_names
    _df.rename(new_names, axis=1, inplace=True, errors="raise")
    _df = _df.reindex(sorted(_df.columns), axis=1)
    return _df


def get_cross_validation_accuracy(no_neighbours, _df):
    train_x_all_samples = _df.reset_index().drop(columns=["user"])
    train_y_all_samples = _df.index

    knn_all_samples = KNeighborsClassifier(no_neighbours)
    sss = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    acc = []
    for train_index, test_index in sss.split(train_x_all_samples, train_y_all_samples):
        knn_all_samples.fit(
            train_x_all_samples.loc[train_index], train_y_all_samples[train_index]
        )
        acc += [
            accuracy_score(
                knn_all_samples.predict(train_x_all_samples.loc[test_index]),
                train_y_all_samples[test_index],
            )
        ]
    return sum(acc) / len(acc)


if __name__ == "__main__":
    with open("data.json", "r") as file:
        u_data = json.loads(file.read())
    intruder_data = {INTRUDER_USERNAME: u_data.pop("Russian_or_Chinese_hacker")}
    df = convert_dict_to_pandas(u_data)

    # Plots
    # Histograms
    plt.figure()
    plt.subplot(1, 3, 1)
    plt.hist(df["HT"])
    plt.title("Hold time histogram")
    plt.subplot(1, 3, 2)
    plt.hist(df["PPT"])
    plt.title("Press-press time histogram")
    plt.subplot(1, 3, 3)
    plt.hist(df["RPT"])
    plt.title("Release-press time histogram")
    plt.tight_layout()

    # Swarm plot
    df = bucket_dataframe(df)
    df_alan = df[df["user"] == "Alan"].sample(n=90)
    df_natasha = df[df["user"] == "Natasha"].sample(n=90)
    df_joel = df[df["user"] == "Joel"].sample(n=90)
    df_giancarlo = df[df["user"] == "Giancarlo"].sample(n=90)
    sample_df = pd.concat([df_alan, df_giancarlo, df_joel, df_natasha])

    plt.figure()
    plt.subplot(3, 1, 1)
    sns.swarmplot(y="HTEnc", x="user", data=sample_df, palette="deep").set_title(
        "Swarm plot of binned hold time"
    )
    plt.subplot(3, 1, 2)
    sns.swarmplot(y="PPTEnc", x="user", data=sample_df, palette="deep").set_title(
        "Swarm plot of binned press-press time"
    )
    plt.subplot(3, 1, 3)
    sns.swarmplot(y="RPTEnc", x="user", data=sample_df, palette="deep").set_title(
        "Swarm plot of binned release-press time"
    )
    plt.tight_layout()

    # Line plot
    # df = convert_to_train(df) # this is for our data
    df = get_test_dataset()

    att_attempts_acc = [get_cross_validation_accuracy(i, df) for i in range(1, 8)]
    plt.figure()
    sns.lineplot(y=att_attempts_acc, x=range(1, 8)).set_title(
        "Cross-Val Accuracy v/s no. of neighbours"
    )
    plt.tight_layout()

    plt.show()
