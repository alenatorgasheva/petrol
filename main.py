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


def main():
    petrol_stations = data_petrol_stations()
    petrol_litres = 45
    filling_time = litres_to_minutes(petrol_litres)


main()
