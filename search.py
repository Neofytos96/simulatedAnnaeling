import re
file = open('Formula_One_1984(1).wmg')
file_list = list(file)


def get_num_of_participants():
    num_of_participants = file_list[0]
    return num_of_participants


get_num_of_participants()


def get_participants_dict():
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
        elif file_list.index(i)>36:
            print(i)
    return (participants_dict)


get_participants_dict()





        # with open('Formula_One_1984(1).wmg', 'r') as reader:
# Read & print the entire file
#     print(reader.readline())