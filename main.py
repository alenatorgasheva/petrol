# Case - study
# This program keeps a report on the operation of the gas station.

# Developers : Daniel A.         (40%),
#              Zemtseva A.       (%),
#              Torgasheva A.     (45%).


import codecs

# Choosing of language.

language = input('Choose your language:\n1. English\n2. Russian\n').lower()
while True:
    if language == 'english' or language == 'en' or \
            language == 'e' or language == '1':
        import lc_en as lc

        break
    elif language == 'russian' or language == 'ru' or \
            language == 'r' or language == '2':
        import lc_ru as lc

        break
    language = input('Please, choose language from proposed: ')
print()


def data_petrol_stations():
    """
    Getting data about petrol stations.
    :return: dictionary with data about petrol stations
    """
    petrol_stations = {}
    with codecs.open('azs.txt', 'r', encoding='UTF-8') as file_in:
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
    with codecs.open('input.txt', 'r', encoding='UTF-8') as file:
        for string in file.readlines():
            applications.append(string.strip())

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


def add_to_queue(application, info_about_petrol_kinds, current_queue, client_lost):
    """
    Function for adding car to queue.
    :param application: application for service
    :param client_lost: number of customers who left the gas station
    :param info_about_petrol_kinds: dictionary with the information about
     kinds of petrol
    :param current_queue: dictionary with the information about current queues
    :return: station
    """
    kind_of_petrol = application.split()[2]
    time = litres_to_minutes(int(application.split()[1]))

    choice = []
    for station in info_about_petrol_kinds[kind_of_petrol]['stations']:
        if current_queue[station]['cars in the queue'] != \
                current_queue[station]['max of queue']:
            choice.append((current_queue[station]['cars in the queue'],
                           station))
    if len(choice) != 0:
        choice.sort()
        station = choice[0][1]
        current_queue[station]['cars in the queue'] += 1
        current_queue[station]['сar ' + str(len(current_queue[station]) - 2 + 1)] = {}
        current_queue[station]['сar ' + str(len(current_queue[station]) - 2)]['time left'] = time
        current_queue[station]['сar ' + str(len(current_queue[station]) - 2)]['car info'] = application

        info_about_petrol_kinds['total amount of petrol'] += \
            int(application.split()[1])
        info_about_petrol_kinds[kind_of_petrol]['amount of petrol'] += \
            int(application.split()[1])

        return station

    else:
        client_lost[0] = client_lost[0] + 1
        print(lc.TXT_LOCKING_QUEUE)
        return


def queue_shift(current_queue):
    """
    The movement of cars in line.
    :param current_queue: dictionary of current queues
    :return: new applications
    """
    current_queue.pop('сar 1')

    if current_queue['cars in the queue'] != 1:
        for car_number in range(1, current_queue['cars in the queue']):
            current_queue['сar ' + str(car_number)] = current_queue['сar ' + str(car_number + 1)].copy()
        current_queue.pop('сar ' + str(current_queue['cars in the queue']))

    current_queue['cars in the queue'] -= 1
    return current_queue


def main():
    client_lost = [0]
    petrol_stations = data_petrol_stations()
    info_about_kinds = info_about_petrol_kinds(petrol_stations)
    current_queue = current_queues(petrol_stations)
    applications = get_applications()

    new_car = applications[0]
    new_car_arrival_time = new_car[:5]
    current_time = '00:00'
    while current_time != '23:59':
        for station in current_queue:
            if current_queue[station]['cars in the queue'] != 0:
                current_queue[station]['сar 1']['time left'] -= 1

                if current_queue[station]['сar 1']['time left'] == 0:
                    print(lc.TXT_CLIENT.format(current_time, current_queue[station]['сar 1']['car info']))
                    current_queue[station] = queue_shift(current_queue[station])
                    for station_number in petrol_stations:
                        print(lc.TXT_QUEUE_STATION.format(station_number, petrol_stations[station_number]['queue'],
                                                          ' '.join(petrol_stations[station_number]['kinds'])), end='')
                        print('*' * current_queue[station_number]['cars in the queue'])
                    print()

        if new_car_arrival_time == current_time:
            update_station = add_to_queue(new_car, info_about_kinds,
                                          current_queue, client_lost)
            print(lc.TXT_NEW_CLIENT.format(current_time, new_car, update_station))

            applications = applications[1:]
            new_car = applications[0]
            new_car_arrival_time = new_car[:5]

            for station in petrol_stations:
                print(lc.TXT_QUEUE_STATION.format(station, petrol_stations[station]['queue'],
                                                  ' '.join(petrol_stations[station]['kinds'])), end='')
                print('*' * current_queue[station]['cars in the queue'])
            print()

        hour, minute = map(int, current_time.split(':'))
        minute += 1
        if minute == 60:
            hour += 1
            minute = 0
        hour = '{:02d}'.format(hour)
        minute = '{:02d}'.format(minute)
        current_time = hour + ':' + minute

    print()
    print(lc.TXT_TOTAL_OF_LITERS,
          info_about_kinds['total amount of petrol'])
    info_about_kinds.pop('total amount of petrol')
    total_revenue = 0

    for kind in info_about_kinds:
        print(lc.TXT_NUM_OF_LITERS.format(kind),
              info_about_kinds[kind]['amount of petrol'])
        revenue = info_about_kinds[kind]['amount of petrol'] * info_about_kinds[kind]['price']
        print(lc.TXT_REVENUE, round(revenue, 2))
        total_revenue += revenue

    print(lc.TXT_TOTAL_REVENUE, round(total_revenue, 2))
    print(lc.TXT_WHO_LEFT, client_lost[0])


main()
