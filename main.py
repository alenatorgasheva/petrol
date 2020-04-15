# Case - study
# This program

# Developers : Daniel A.         (%),
#              Zemtseva A.       (%),
#              Torgasheva A.     (%).

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
            station_number = string[0]
            queue_length = string[1]
            petrol_stations[station_number] = {}
            petrol_stations[station_number]['queue'] = queue_length
            petrol_stations[station_number]['kinds'] = string[2:]

    return petrol_stations


def main():
    petrol_stations = data_petrol_stations()


main()
