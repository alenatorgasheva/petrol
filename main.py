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
import math


def data_petrol_stations():
    """
    Getting data about petrol stations.
    :return: dictionary with data about petrol stations
    """
    petrol_stations = {}
    with codecs.open('azs.txt', 'r', encoding='windows-1251') as file_in:
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
    with codecs.open('input.txt', 'r', encoding='windows-1251') as file:
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


def info_about_petrol_kinds(petrol_stations):
    """
    Function for making dictionary with the information about kinds of petrol
     (price, amount of petrol, numbers of petrol stations with this kind) from
      dictionary with the information about petrol stations.
    :param petrol_stations: dictionary with the information about petrol stations
    :return: dictionary with the information about kinds of petrol
    """
    info_about_petrol_kinds = {}
    info_about_petrol_kinds['total amount of petrol'] = 0

    for number_of_petrol in petrol_stations:
        for petrol_name in petrol_stations[number_of_petrol]['kinds']:
            if petrol_name not in info_about_petrol_kinds:
                info = {}
                if petrol_name == 'АИ-80':
                    price = 38.95
                elif petrol_name == 'АИ-92':
                    price = 43.01
                elif petrol_name == 'АИ-95':
                    price = 45.69
                elif petrol_name == 'АИ-98':
                    price = 49.2
                info['price'] = price
                info['stations'] = [number_of_petrol]
                info['amount of petrol'] = 0
                info_about_petrol_kinds[petrol_name] = info
            else:
                info = info_about_petrol_kinds[petrol_name]
                info['stations'] = info['stations'] + [number_of_petrol]
    return info_about_petrol_kinds


def current_queues(petrol_stations):
    """
    Function for making dictionary with the information about current queues
     (cars in the queue,max of queue) from dictionary with the information
      about petrol stations.
    :param petrol_stations: dictionary with the information about petrol stations
    :return: dictionary with the information about current queues
    """
    current_queues = {}
    for number_of_station in petrol_stations:
        info = {}
        info['cars in the queue'] = 0
        info['max of queue'] = petrol_stations[number_of_station]['queue']
        current_queues[number_of_station] = info
    return current_queues


def add_to_queue(application, info_about_petrol_kinds, current_queue):
    """
    Function for adding car to queue.
    :param application: application for service
    :param info_about_petrol_kinds: dictionary with the information about
     kinds of petrol
    :param current_queue: dictionary with the information about current queues
    :return: None
    """
    # application - это одна строка из applications типа '00:12 40 АИ-92'
    kind_of_petrol = application.split()[2]
    time = math.ceil(int(application.split()[1]) / 10)
    choice = []
    # Очереди формируются по закону – новый автомобиль добавляется только в очередь к автомату,
    # если это автомат способен заправить автомобиль необходимой маркой бензина.
    # Из всех таких автоматов выбирается тот, у которого меньше очередь.
    for station in info_about_petrol_kinds[kind_of_petrol]['stations']:
        if current_queue[station]['cars in the queue'] !=\
                current_queue[station]['max of queue']:
            choice.append((current_queue[station]['cars in the queue'],
                           station))
    if len(choice) != 0:
        choice.sort()
        station = choice[0][1]
        # добавляем в очередь
        current_queue[station]['cars in the queue'] += 1
        current_queue[station]['сar ' + str(len(current_queue[station]) - 2 + 1
                                            )] = time
        # из-за того, что машина встала в очередь меняется 'total amount of petrol' и 'amount of petrol'
        info_about_petrol_kinds['total amount of petrol'] +=\
            int(application.split()[1])
        info_about_petrol_kinds[kind_of_petrol]['amount of petrol'] +=\
            int(application.split()[1])
        return

    else:
        print('машина уехала, т к все очереди макс')
        return

def main():
    petrol_stations = data_petrol_stations()
    info_about_kinds = info_about_petrol_kinds(petrol_stations)
    current_queue = current_queues(petrol_stations)
    petrol_litres = 45
    filling_time = litres_to_minutes(petrol_litres)
    add_to_queue('00:12 40 АИ-92',info_about_kinds,current_queue)
    print(current_queue)
    print(petrol_stations)
    print(info_about_kinds)


main()
