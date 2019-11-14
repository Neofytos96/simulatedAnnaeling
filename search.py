import re
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
        self.weight = weight
        self.driver_won = driver_won
        self.driver_lost = driver_lost

results_list=[]

def get_participants_details():
    participants_dict = {}
    for i in file_list:
        # to skip the first entry
        if 0 < file_list.index(i) < 36:
            # print(i)
            x = re.split("\,", i)
            driver_id = int(x[0])
            driver_name = x[1].strip()
            # print(driver_name)
            # print(driver_id)
            participants_dict[driver_id] = driver_name
        # get the results for each driver
        elif file_list.index(i)>36:
            x = re.split("\,", i)
            weight_of_win = int(x[0])
            driver_won = int(x[1])
            driver_lost = int(x[2])
            results_list.append(results_class(weight_of_win,driver_won,driver_lost))
    return (participants_dict, results_list)


get_participants_details()

for i in results_list:
    print(i.driver_lost)



        # with open('Formula_One_1984(1).wmg', 'r') as reader:
# Read & print the entire file
#     print(reader.readline())