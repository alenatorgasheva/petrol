# Case - study
# This program

# Developers : Daniel A.         (%),
#              Zemtseva A.       (%),
#              Torgasheva A.     (%).

# {'1':     {'queue' : '3',
#            'kinds' : ['АИ-80']},
#  '2':     {'queue' : '2',
#            'kinds' : ['АИ-92']},
#  '3':     {'queue' : '4',
#            'kinds' : ['АИ-92', 'АИ-95', 'АИ-98']}}

import codecs


def data_petrol_stations():
    """
    Getting data about petrol stations.
    :return: dictionary with data about petrol stations
    """
    petrol_stations = {}
    with codecs.open('azs.txt', 'r', encoding='utf-8') as file_in:
        for string in file_in.readlines():
            string = string.split()
            station_number = int(string[0])
            queue_length = int(string[1])
            petrol_stations[station_number] = {}
            petrol_stations[station_number]['queue'] = queue_length
            petrol_stations[station_number]['kinds'] = string[2:]

    return petrol_stations


def litres_to_minutes(litres):
    """
    Counting filling time.
    :param litres: petrol quantity
    :return: filling time
    """
    import random

    if litres % 10 != 0:
        litres = (litres // 10 + 1) * 10
    minutes = litres // 10

    change = random.randint(-1, 1)
    if minutes + change != 0:
        minutes += change

    return minutes


def get_applications():
    """
    Reading data from a file line by line and writing to a list.
    :return: list of applications
    """
    applications = []
    with codecs.open('input.txt', 'r', encoding='utf-8') as file:
        for string in file.readlines():
            applications.append(string.strip())

    return applications

def get_least_queue(dir_3):
    """
    Finding the least queue.
    :param dir_3: current lines
    :return: least queue
    """
    # Словарь 3 которого еще нет
    # dir_3 = {1: {'сколько машин в очереди': 3, 'машина 1': 10, 'машина 2': 30, 'машина 3': 40},
    #      2: {'сколько машин в очереди': 2, 'машина 1': 20, 'машина 2': 30},
    #      3: {'сколько машин в очереди': 2, 'машина 1': 20, 'машина 2': 30}}
    min_val = []
    line = {}
    for key, val in dir_3.items():
        for k, v in val.items():
            if k == 'сколько машин в очереди':
                line[key] = val[k]
    for value in line.values():
        min_val.append(value)
    min_l = min(min_val)

    new_line = {}
    for key, value in line.items():
        new_line[value] = key
    least_queue = new_line[min_l]
    return least_queue


def queue_shift(dir_3, applications):
    """
    The movement of cars in line.
    :param dir_3: current lines
    :param applications: list of applications
    :return: new applications
    """
    for value in dir_3.values():
        for k, v in value.items():
            if k == 'машина 1' and v == 0:
                applications.pop(0)
    return applications


def main():
    petrol_stations = data_petrol_stations()
    petrol_litres = 45
    filling_time = litres_to_minutes(petrol_litres)


main()
