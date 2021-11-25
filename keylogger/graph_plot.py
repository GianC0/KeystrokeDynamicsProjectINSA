import matplotlib.pyplot as matp
import matplotlib as mpl
import data_processer as dp


mpl.rcParams['figure.dpi'] = 300
users = {"Giancarlo": (0, 0), "Alan": (0, 1), "Joel": (1, 0), "Natasha": (1, 1)}
keys = ["press_press_df", "release_release_df", "release_press_df"]
raw_data = dp.get_processed_data()

fig, axes = matp.subplots(nrows=2, ncols=2, figsize=(16, 9))
fig.suptitle("hold_time")
for user in users.keys():
    df = raw_data[user]["hold_time_df"]
    df.boxplot(ax=axes[users[user]], showfliers=False)
    axes[users[user]].set_title(user)
matp.show()

for key in keys:
    fig, axes = matp.subplots(nrows=2, ncols=2, figsize=(16, 9))
    fig.suptitle(key)
    for user in users:
        df = raw_data[user][key]
        df.boxplot(ax=axes[users[user]], showfliers=False)
        axes[users[user]].set_xticklabels(df.columns, rotation=60)
        axes[users[user]].set_title(user)
    matp.show()