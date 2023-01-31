from user import User
from utils import distance_km


def cp2_1_simple_inference(dictUsers):
    dictUsersInferred = dict()  # dict to return, store inferred results here
    # you should keep everything in dictUsers as is / read-only
    # TODO
    return dictUsersInferred


def cp2_2_improved_inference(dictUsers):
    dictUsersInferred = dict()
    # TODO
    return dictUsersInferred


def cp2_calc_accuracy(truth_dict, inferred_dict):
    # distance_km(a,b): return distance between a and be in km
    # recommended standard: is accuate if distance to ground truth < 25km
    if len(truth_dict) != len(inferred_dict) or len(truth_dict)==0:
        return 0.0
    sum = 0
    for i in truth_dict:
        if truth_dict[i].home_shared:
            sum += 1
        elif truth_dict[i].latlon_valid() and inferred_dict[i].latlon_valid():
            if distance_km(truth_dict[i].home_lat, truth_dict[i].home_lon, inferred_dict[i].home_lat,
                           inferred_dict[i].home_lon) < 25.0:
                sum += 1
    return sum * 1.0 / len(truth_dict)
