import math
import data_processer


data = data_processer.get_processed_data()

def euclidean_distance(array1, array2):
    distance = 0.0
    for i in range(len(array1) - 1):
        distance += (array1[i] - array2[i]) ** 2
    return math.sqrt(distance)


def calculate_distances():
    user_1 = data.get('Alan') #User to compare all the others with
    print(user_1)
    # for user in data:

calculate_distances()