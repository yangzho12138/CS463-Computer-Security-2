from user import User
from utils import distance_km
import numpy as np


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
                user = User(u_id=v.id, u_home_shared=False)
            dictUsersInferred.update(((v.id, user),))
        else:
            dictUsersInferred.update(((v.id, v),))
    return dictUsersInferred


def cp2_2_improved_inference(dictUsers):
    dictUsersInferred = dict()
    for v in dictUsers.values():
        if v.home_shared == False:
            frnShareLoc = 0
            frnShareBound = 3
            frn_home_loc = []
            for f in v.friends:
                frn = dictUsers[f]
                if frn.home_shared == True:
                    frnShareLoc += 1
                    frn_home_loc.append([frn.home_lat, frn.home_lon])

            if frnShareLoc < frnShareBound:
                for f in v.friends:
                    if frnShareLoc >= frnShareBound:
                        break
                    for ff in dictUsers[f].friends:
                        ffrn = dictUsers[ff]
                        if ffrn.home_shared == True:
                            frnShareLoc += 1
                            frn_home_loc.append([ffrn.home_lat, ffrn.home_lon])
                        # else:
                        #     if dictUsersInferred.__contains__(ff):
                        #         ffrnInferred = dictUsersInferred[ff]
                        #         if ffrnInferred.home_shared == True:
                        #             frnShareLoc += 1
                        #             frn_home_loc.append(
                        #                 [ffrnInferred.home_lat, ffrnInferred.home_lon])
                        if frnShareLoc >= frnShareBound:
                            break
            # find the outlier
            if frn_home_loc != []:
                frn_home_loc = np.array(frn_home_loc)
                mean = np.mean(frn_home_loc, axis=0)
                meanLat = mean[0]
                meanLon = mean[1]
                sd = np.std(frn_home_loc, axis=0)
                sdLat = sd[0]
                sdLon = sd[1]
                # float64 accuracy problem +- 10e-8
                withoutOutlierList = [[x, y] for [x, y] in frn_home_loc if (
                    (x > meanLat - 1*sdLat - 10e-8 and x < meanLat + 1*sdLat + 10e-8) and (y > meanLon - 1*sdLon - 10e-8 and y < meanLon + 1*sdLon + 10e-8))]
                if len(withoutOutlierList) != 0:
                    latSum = 0
                    lonSum = 0
                    for [lat, lon] in withoutOutlierList:
                        latSum += lat
                        lonSum += lon
                    user = User(v.id, latSum/len(withoutOutlierList),
                                lonSum/len(withoutOutlierList), True)
                    dictUsersInferred.update(((v.id, user),))
                else:
                    user = User(v.id, meanLat, meanLon, True)
                    dictUsersInferred.update(((v.id, user),))
            else:
                user = User(u_id=v.id, u_home_shared=False)
                dictUsersInferred.update(((v.id, user),))
        else:
            dictUsersInferred.update(((v.id, v),))

    return dictUsersInferred


def cp2_calc_accuracy(truth_dict, inferred_dict):
    # distance_km(a,b): return distance between a and be in km
    # recommended standard: is accuate if distance to ground truth < 25km
    if len(truth_dict) != len(inferred_dict) or len(truth_dict) == 0:
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
