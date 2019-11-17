import operator
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


# from collections import defaultdict
#
# result_analytics = defaultdict(int)
# for i in results_list:
#     result_analytics[i.get_driver_won()] += i.get_weight()
#     import collections
#
# sorted_list_on_analytics = sorted(result_analytics, key=result_analytics.get, reverse=True)


def find_neighbourhood(ranking):

    random_result_object = (random.choice(results_list))
    num_a = random_result_object.get_driver_won()
    num_b = random_result_object.get_driver_lost()
    if ranking.index(num_a)>ranking.index(num_b):
        swap(num_a, num_b, ranking)
    else:
        find_neighbourhood(ranking)

    # num_a = random.randint(1,35)
    # num_b = random.randint(1, 35)
    # num_c = random.randint(1,35)
    # for i in results_list:
    #     if i.get_driver_won()==num_a and i.get_driver_lost()== num_b:
    #         swap(num_a, num_b, ranking)
    #     elif i.get_driver_won()==num_a and i.get_driver_lost()== num_c:
    #         swap(num_a,num_c,ranking)
    #     elif i.get_driver_won()==num_b and i.get_driver_lost()== num_c:
    #         swap(num_b,num_c,ranking)
    #
    #     elif i.get_driver_won()==num_b and i.get_driver_lost()== num_a:
    #         swap(num_b,num_a,ranking)
    #     elif i.get_driver_won()==num_c and i.get_driver_lost()== num_a:
    #         swap(num_c,num_a,ranking)
    #     elif i.get_driver_won()==num_c and i.get_driver_lost()== num_b:
    #         swap(num_b,num_c,ranking)



    # if num_a!=num_b:
    #     swap(num_a,num_b,ranking)
    return ranking


def swap(num_a, num_b, ranking):
    ranking[ranking.index(num_a)], ranking[ranking.index(num_b)] = ranking[ranking.index(num_b)], ranking[
        ranking.index(num_a)]


initial_temp = 100000000000
temp_length = 10000
stopping_count = 0
for i in range(temp_length):

    if i % 1000 == 0:
        print(get_kemeny_ranking(participant_nums))
    previous_state = participant_nums
    previous_cost = get_kemeny_ranking(previous_state[:])
    next_state = find_neighbourhood(previous_state[:])
    next_cost = get_kemeny_ranking(next_state)

    if previous_cost > next_cost:
        participant_nums = next_state
        min_cost = next_cost
        stopping_count = 0

    else:
        q = random.random()
        stopping_count += 1
        if q < math.exp(-(next_cost - previous_cost) / initial_temp):
            participant_nums = next_state
            min_cost = next_cost
    initial_temp = initial_temp * 0.996

    if stopping_count == 2000:
        print("stopping criterion")
        break
print(participant_nums)
print(min_cost)
