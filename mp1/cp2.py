from user import User
from utils import distance_km


def cp2_1_simple_inference(dictUsers):
    dictUsersInferred = dict()  # dict to return, store inferred results here
    # you should keep everything in dictUsers as is / read-only
    for v in dictUsers.values():
        if v.home_shared == False:
            latSum = 0
            lonSum = 0
            frnShareLoc = 0
            for f in v.friends:
                frn = dictUsers[f]
                if frn.home_shared == True:
                    latSum += frn.home_lat
                    lonSum += frn.home_lon
                    frnShareLoc += 1
            if frnShareLoc != 0:
                user = User(v.id, latSum/frnShareLoc, lonSum/frnShareLoc, True)
            else:
                user = User(u_id = v.id, u_home_shared = False)
            dictUsersInferred.update(((v.id, user),))
        else:
            dictUsersInferred.update(((v.id, v),))
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
