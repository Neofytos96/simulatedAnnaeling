import re
from random import seed
import random
import math

file = open('Formula_One_1984(1).wmg')
file_list = list(file)


def get_num_of_participants():
    num_of_participants = file_list[0]
    return num_of_participants


get_num_of_participants()


class results_class(object):
    # driver_won = int
    # weight = int
    # driver_lost = int

    def __init__(self, weight, driver_won, driver_lost):
        self._weight = weight
        self._driver_won = driver_won
        self._driver_lost = driver_lost

    # getter method
    def get_weight(self):
        return self._weight

    # getter method
    def get_driver_won(self):
        return self._driver_won  # getter method

    def get_driver_lost(self):
        return self._driver_lost


def get_participants_details():
    participants_dict = {}
    results_list = []
    initial_ranking = []
    for i in file_list:
        # to skip the first entry
        if 0 < file_list.index(i) < 36:
            # print(i)
            x = re.split("\,", i)
            driver_id = int(x[0])
            driver_name = x[1].strip()
            # print(driver_name)
            # print(driver_id)
            initial_ranking.append(driver_id)
            participants_dict[driver_id] = driver_name
        # get the results for each driver
        elif file_list.index(i) > 36:
            x = re.split("\,", i)
            weight_of_win = int(x[0])
            driver_won = int(x[1])
            driver_lost = int(x[2])
            results_list.append(results_class(weight_of_win, driver_won, driver_lost))
    return (participants_dict, results_list, initial_ranking)


get_participants_details()
file.close()

participant_nums = get_participants_details()[2]
results_list = get_participants_details()[1]
# print(results_list)

# print(initial_ranking)


def get_kemeny_ranking(list):
    kemeny_score = 0
    for i in results_list:
        if (list.index(i.get_driver_won()) > list.index(i.get_driver_lost())):
            # print(i.get_driver_won(), "swap with: ", i.get_driver_lost())
            kemeny_score += i.get_weight()
    return (kemeny_score)


def swap(ranking):
    # for i in results_list:
    #     if (ranking.index(i.get_driver_won()) > ranking.index(i.get_driver_lost())):
    #         ranking[ranking.index(i.get_driver_won())], ranking[ranking.index(i.get_driver_lost())]=\
    #             ranking[ranking.index(i.get_driver_lost())], ranking[ranking.index(i.get_driver_won())]
    num_a = random.randint(1, 35)
    num_b = random.randint(1, 35)
    ranking[ranking.index(num_a)], ranking[ranking.index(num_b)]= ranking[ranking.index(num_b)],ranking[ranking.index(num_a)]
    return ranking


# for i in results_list:
#     if (initial_ranking.index(i.get_driver_won()) > initial_ranking.index(i.get_driver_lost())):
#             new_list = swap(initial_ranking.index(i.get_driver_won()),initial_ranking.index(i.get_driver_lost()), initial_ranking)
#             if get_kemeny_ranking(initial_ranking)<get_kemeny_ranking(new_list):
#                 initial_ranking=new_list

    # print(get_kemeny_ranking(new_list))
# print(get_kemeny_ranking())


initial_temp = 100000000
temp_length = 10000
for i in range(temp_length):
    if i % 100 == 0:
        print(get_kemeny_ranking(participant_nums))
    previous_state = participant_nums
    previous_cost = get_kemeny_ranking(previous_state[:])
    next_state = swap(previous_state[:])
    next_cost = get_kemeny_ranking(next_state)


    if previous_cost > next_cost:
        participant_nums= next_state

    else:
        q = random.random()

        if q < math.exp(-(next_cost- previous_cost)/initial_temp):
            print("q: ",q)
            print("e: ",math.exp(-(next_cost - previous_cost) / initial_temp))
            participant_nums = next_state
    initial_temp = initial_temp * 0.9
    print(previous_cost, next_cost)


            # if (nextEnergy < minEnergy) {
    # minState
    # = (State) state.clone();
    # minEnergy = nextEnergy;
    # }
    # }
    # else
    # state.undo();
    # }
    # return minState;
# }















