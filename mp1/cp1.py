import csv
from logging import warn, error, debug
from user import User

## parse homes.txt
#  input:
#    f: filename
#  output:
#    a dict of all users from homes.txt with key=user_id, value=User object
def cp1_1_parse_homes(f):
    dictUsers_out = dict()
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            id = int(i[0])
            if len(i) > 1:
                home_lat = float(i[1].strip())
                home_lon = float(i[2].strip())
                home_shared = bool(int(i[3].strip()))
                user = User(id, home_lat, home_lon, home_shared)
            else:
                user = User(u_id = id, u_home_shared = False)
            dictUsers_out.update(((id, user),))
    return dictUsers_out


## parse friends.txt
#  input:
#    f: filename
#    dictUsers: dictionary of users, output of cp1_1_parse_homes()
#  no output, modify dictUsers directly
def cp1_2_parse_friends(f, dictUsers):
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            user1 = int(i[0].strip())
            user2 = int(i[1].strip())
            dictUsers[user1].friends.add(user2)
            dictUsers[user2].friends.add(user1)


# return all answers to Checkpoint 1.3 of MP Handout in variables
# order is given in the template
def cp1_3_answers(dictUsers):
    u_cnt = len(dictUsers)
    u_noloc_cnt = 0
    u_noloc_nofnds_cnt = 0
    u_noloc_nofnds_nofndshare_cnt = 0
    for v in dictUsers.values():
        if v.home_shared == False:
            u_noloc_cnt += 1
            if len(v.friends) == 0:
                u_noloc_nofnds_cnt += 1
                u_noloc_nofnds_nofndshare_cnt += 1
            else:
                flag = True
                for f in v.friends:
                    # someone shared the location
                    if dictUsers[f].home_shared == True:
                        flag = False
                        break
                if flag:
                    u_noloc_nofnds_nofndshare_cnt += 1       
    p_b = format(float(u_cnt - u_noloc_cnt)/float(u_cnt), '.2f')       
    p_u1 = format(float(u_cnt - u_noloc_nofnds_cnt)/float(u_cnt), '.2f')     
    p_u2 = format(float(u_cnt - u_noloc_nofnds_nofndshare_cnt)/float(u_cnt), '.2f')
    return u_cnt, u_noloc_cnt, u_noloc_nofnds_cnt, p_b, p_u1, p_u2
