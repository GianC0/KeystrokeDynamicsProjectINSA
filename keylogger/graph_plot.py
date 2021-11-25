import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as matp
import data_processer as dp

columns = list('the quick brown fox jumps over the lazy dog.')

def get_DataFrame(user):
    sentences=dp.get_processed_data()[user]['raw_data']
    data=[]
    for sentence in sentences:
        times = []
        for press_item in sentence:
            if ' PRESS' in press_item:
                timeI, letterI = press_item[0], press_item[1].replace("'", '').strip().casefold()
                for release_item in sentence[sentence.index(press_item)+1:]:
                    # this includes the capital T at the beginning
                    if letterI == release_item[1].replace("'",'').strip().casefold() and ' RELEASE' in release_item:  #or (letterI.lower() + ',' + ' RELEASE' in release_item):
                        timeF = release_item[0]
                        times.append(int(timeF)-int(timeI))
                        break
        data.append(times)
    return pd.DataFrame(data,columns=columns)


fig, axes = matp.subplots(nrows=2, ncols=2,figsize=(16,9))

users = {"Giancarlo":(0,0), "Alan":(0,1), "Joel":(1,0), "Natasha":(1,1) }
for user in users.keys():
    df = get_DataFrame(user)
    df.boxplot(ax=axes[users[user]])
    axes[users[user]].set_title(user)

matp.show()

