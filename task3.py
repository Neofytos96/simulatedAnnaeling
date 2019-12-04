from task2 import simulated_annealing

import time
import pandas as pd
import csv


# run command python3 task3.py Formula_One_1984.wmg
# and uncomment the method you want to test


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
    with open("statistics4.csv", "w") as out_file:
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

# reads the file that is created in the statistical_analysis.py that includes
# the best kemeny scores achieved from the generate_data() method
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
                        with open("best_result_analysis.csv", "a") as out_file:
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
    best_data = pd.read_csv('best_result_analysis.csv')
    best_data = best_data.dropna()
    filtering = (best_data.kemeny_score < 65)
    filtered_data = best_data[filtering]
    print(filtered_data)


# print_best_variables()
