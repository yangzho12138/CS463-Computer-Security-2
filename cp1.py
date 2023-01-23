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
            # TODO
    return dictUsers_out


## parse friends.txt
#  input:
#    f: filename
#    dictUsers: dictionary of users, output of cp1_1_parse_homes()
#  no output, modify dictUsers directly
def cp1_2_parse_friends(f, dictUsers):
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            # TODO


# return all answers to Checkpoint 1.3 of MP Handout in variables
# order is given in the template
def cp1_3_answers(dictUsers):
    # TODO: return your answers as variables in the given order
    return u_cnt, u_noloc_cnt, u_noloc_nofnds_cnt, p_b, p_u1, p_u2
