import re
import random
import math
import sys
import time

# command to run the code: python3 task2.py Formula_One_1984.wmg

file = open(str(sys.argv[1]))

file_list = list(file)


# getting the number of participants by reading the first line of csv file
def get_num_of_participants():
    num_of_participants = file_list[0]
    return num_of_participants


get_num_of_participants()


# declare the weights and edges list as a list of objects
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


# retrieve all the usefull information from the csv file
# and store them into 3 lists that they are returned from the method

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


# calculate the kemeny score of a particular ranking
def get_kemeny_ranking(list):
    kemeny_score = 0
    for i in results_list:
        if (list.index(i.get_driver_won()) > list.index(i.get_driver_lost())):
            kemeny_score += i.get_weight()
    return (kemeny_score)


# incrementally calculate the kemeny score of the new ranking based on the previous kemeny score
# used the method described in the report in task 1
def increment_kemeny_ranking(previous_state, next_state):
    kemeny_difference = 0
    index_changes = [(previous_state[i]) for i in range(len(previous_state)) if previous_state[i] != next_state[i]]

    influenced_drivers = []
    for i in range(previous_state.index(index_changes[0]), previous_state.index(index_changes[1]) - 1):
        influenced_drivers.append(previous_state[i + 1])

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
            if (next_state.index(i.get_driver_won()) > next_state.index(i.get_driver_lost())):
                kemeny_difference += i.get_weight()

            else:

                kemeny_difference -= i.get_weight()
    return kemeny_difference


# find a neighborhood by selecting a random record from the weights
# and edges list and then checking their ranks in the current ranking table
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
    initial_temp = initial_temperature
    temp_length = temperature_length
    stopping_count = 0
    uphill_counter = 0
    best_state = participant_nums

    # Those are the steps that of the simulated annealing algorithm
    for i in range(temp_length):

        previous_state = participant_nums
        previous_cost = get_kemeny_ranking(previous_state[:])

        next_state = find_neighbourhood(previous_state[:])
        next_cost = previous_cost + increment_kemeny_ranking(previous_state, next_state)

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
                uphill_counter += 1
        initial_temp = initial_temp * a

        if stopping_count == num_non_improve:
            break

    return min_cost, participant_nums, uphill_counter


start_time = time.time()
# parameters: initial_temperature, temperature_length, a, num_non_improve
simulated_annealing(1000, 10000, 0.996, 3000)
end_time = time.time()

rank_counter = 1
print("Rank", "   Name")
for counter, drivers in enumerate(participant_nums, 1):
    print("---------------------------|")
    print(counter, "    ", participant_dict[drivers])

print("---------------------------|\n")

print("Kemeny score of solution found: ", min_cost)
print("Algorithm Runtime (in milliseconds):", round((end_time - start_time) * 1000, 2))
print("Uphill moved made: ", uphill_counter)
