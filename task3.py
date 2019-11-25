import re
import random
import math
import sys
import time

import pandas as pd
from texttable import Texttable
import csv


# command to run the code: python3 search.py Formula_One_1984.wmg

# file = open(str(sys.argv[1]))

file = open('Formula_One_1984.wmg')
file_list = list(file)


def get_num_of_participants():
    num_of_participants = file_list[0]
    return num_of_participants


get_num_of_participants()


class results_class(object):
    def __init__(self, weight, driver_won, driver_lost):
        self._weight = weight
        self._driver_won = driver_won
        self._driver_lost = driver_lost

    # getter method
    def get_weight(self):
        return self._weight

    # getter method
    def get_driver_won(self):
        return self._driver_won

    def get_driver_lost(self):
        return self._driver_lost


def get_participants_details():
    participants_dict = {}
    results_list = []
    initial_ranking = []
    for i in file_list:
        # to skip the first entry
        if 0 < file_list.index(i) < 36:
            x = re.split("\,", i)
            driver_id = int(x[0])
            driver_name = x[1].strip()
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
participant_dict = get_participants_details()[0]
participant_nums = get_participants_details()[2]
results_list = get_participants_details()[1]


def get_kemeny_ranking(list):
    kemeny_score = 0
    for i in results_list:
        if (list.index(i.get_driver_won()) > list.index(i.get_driver_lost())):
            kemeny_score += i.get_weight()
    return (kemeny_score)


def increment_kemeny_ranking(previous_state, next_state):
    kemeny_difference = 0
    index_changes = [(previous_state[i]) for i in range(len(previous_state)) if previous_state[i] != next_state[i]]

    influenced_drivers = []
    for i in range(previous_state.index(index_changes[0]), previous_state.index(index_changes[1]) - 1):
        # print(previous_state[i+1])

        influenced_drivers.append(previous_state[i + 1])
    # print(previous_state)
    # print(next_state)
    # print("index drivers:", index_changes)
    # print("influenced drivers:", influenced_drivers)
    # index_changes = set(index_changes)

    for i in results_list:
        if i.get_driver_won() in index_changes and i.get_driver_lost() in influenced_drivers:
            if (next_state.index(i.get_driver_won()) > next_state.index(i.get_driver_lost())):
                kemeny_difference += i.get_weight()
            else:
                kemeny_difference -= i.get_weight()

        elif i.get_driver_lost() in index_changes and i.get_driver_won() in influenced_drivers:
            if (next_state.index(i.get_driver_won()) > next_state.index(i.get_driver_lost())):
                kemeny_difference += i.get_weight()

            else:

                kemeny_difference -= i.get_weight()

        elif i.get_driver_won() in index_changes and i.get_driver_lost() in index_changes:
            # print("here")
            if (next_state.index(i.get_driver_won()) > next_state.index(i.get_driver_lost())):
                kemeny_difference += i.get_weight()
                # print("Adding:", i.get_driver_won(), i.get_driver_lost())

            else:
                # print("Subtracting:", i.get_driver_won(), i.get_driver_lost())

                kemeny_difference -= i.get_weight()
                # else:
                # print("driver won: ",i.get_driver_won())
                # print("driver lost:", i.get_driver_lost())
                # print(next_state)
    # print(kemeny_difference)
    return kemeny_difference


def find_neighbourhood(ranking):
    random_result_object = (random.choice(results_list))
    num_a = random_result_object.get_driver_won()
    num_b = random_result_object.get_driver_lost()
    if ranking.index(num_a) > ranking.index(num_b):
        swap(num_a, num_b, ranking)
    else:
        find_neighbourhood(ranking)
    return ranking


def swap(num_a, num_b, ranking):
    ranking[ranking.index(num_a)], ranking[ranking.index(num_b)] = ranking[ranking.index(num_b)], ranking[
        ranking.index(num_a)]


def simulated_annealing(initial_temperature, temperature_length, a, num_non_improve):
    global participant_nums, min_cost, uphill_counter, best_state
    min_cost = get_kemeny_ranking(participant_nums)
    initial_temp = initial_temperature  # 100000000000
    temp_length = temperature_length  # 10000
    stopping_count = 0
    uphill_counter = 0
    best_state = participant_nums
    for i in range(temp_length):

        # if i % 1000 == 0:
        #     print(min_cost)

        previous_state = participant_nums
        previous_cost = get_kemeny_ranking(previous_state[:])

        next_state = find_neighbourhood(previous_state[:])
        next_cost = previous_cost + increment_kemeny_ranking(previous_state, next_state)
        # print("calculated:", previous_cost + increment_kemeny_ranking(previous_state, next_state))
        # print("correct:", get_kemeny_ranking(next_state))

        if previous_cost > next_cost:
            participant_nums = next_state
            if next_cost < min_cost:
                min_cost = next_cost
                best_state = participant_nums[:]
                stopping_count = 0


        else:
            q = random.random()
            stopping_count += 1
            if q < math.exp(-(next_cost - previous_cost) / initial_temp):
                participant_nums = next_state
                # min_cost = next_cost
                uphill_counter += 1
        initial_temp = initial_temp * a  # 0.998  # 0.996

        if stopping_count == num_non_improve:  # 3000:
            break

    return min_cost, participant_nums, uphill_counter


# results = simulated_annealing(1000,10000, 0.998,2000)

# min_cost  = results[0]

def generate_data():
    initial_temperature_list = []
    temperature_length_list = []
    a_list = []
    num_non_improve_list = []
    time_list = []
    kemeny_list = []
    temp_length_constant = 10000
    num_non_improve_constant = 2000
    index = 0
    with open("statistic4.csv", "w") as out_file:
        # for i in range(3):
        for initial_temp in [100, 1000, 100000, 1000000, 10000000, 100000000]:
            for a_value in range(990, 999):
                for temp_length in [100, 1000, 10000, 100000]:
                    for num_non_improve in [1000, 2000, 3000]:
                        cooling_multiple = a_value / 1000
                        for i in range(3):
                            kemeny_list_results = []
                            time_results = []
                            start_time = time.time()
                            results = simulated_annealing(initial_temp,
                                                          temp_length,
                                                          cooling_multiple,
                                                          num_non_improve)
                            end_time = time.time()
                            time_taken = end_time - start_time
                            kemeny_list_results.append(results[0])
                            time_results.append(time_taken)

                        out_string = "\r\n"
                        out_string += str(initial_temp)
                        out_string += "," + str(cooling_multiple)
                        out_string += "," + str(temp_length)
                        out_string += "," + str(num_non_improve)
                        out_string += "," + str(sum(time_results) / len(time_results))
                        out_string += "," + str(sum(kemeny_list_results) / len(kemeny_list_results))
                        out_file.write(out_string)
                        print(index)
                        index += 1

        out_file.close()


# generate_data()


def generate_best_cases_results():
    global line_count, row
    with open('bestCases.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        # with open("best_result_analysis.csv", "w") as out_file:

        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                kemeny_result_list = []
                for_loop_counter = 0
                for i in range(10):
                    for_loop_counter += 1
                    initial_temp = int(row[1])
                    cooling_multiple = float(row[2])
                    temp_length = int(row[3])
                    num_non_improve = int(row[4])

                    result = simulated_annealing(initial_temp, temp_length, cooling_multiple, num_non_improve)
                    kemeny_result_list.append(result[0])
                    if for_loop_counter == 10:
                        with open("best_result_analysis2.csv", "a") as out_file:
                            out_string = "\r\n"
                            out_string += str(initial_temp)
                            out_string += "," + str(cooling_multiple)
                            out_string += "," + str(temp_length)
                            out_string += "," + str(num_non_improve)
                            # out_string += "," + str(sum(time_results) / len(time_results))
                            out_string += "," + str(sum(kemeny_result_list) / len(kemeny_result_list))
                            out_file.write(out_string)
                            out_file.close()
                print(f'\t{row[1]} ,{row[2]} ,{row[3]}, {row[4]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')


# generate_best_cases_results()

def print_best_variables():
    best_data = pd.read_csv('best_result_analysis2.csv')
    best_data = best_data.dropna()
    filtering = (best_data.kemeny_score < 65)
    filtered_data = best_data[filtering]
    print(filtered_data)


# print_best_variables()
