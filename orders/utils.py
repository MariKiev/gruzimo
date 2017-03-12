import logging
from decimal import Decimal

import googlemaps

from django.conf import settings

logger = logging.getLogger(__name__)


class CalculateCostError(Exception):
    def __init__(self, message):
        self.message = message


def get_order_cost(data):
    size = calculate_size(data.get('length'), data.get('width'), data.get('height'))
    print(data.get('from_address'))
    print(data.get('to_address'))

    if "Киев, город Киев" not in data.get("to_address") and 'Киев, город Киев' not in data.get('from_address'):
        distance, duration = get_distance(data.get('from_address'), data.get("to_address"))
    elif 'Київ, Украина' not in data.get("to_address") and 'Київ, Украина' not in data.get('from_address'):
        distance, duration = get_distance(data.get('from_address'), data.get("to_address"))
    else:
        distance = None
        duration = None

    if size < 9:
        cost = class_1_cost(distance, duration)
    elif 9 <= size < 23:
        cost = class_2_cost(distance, duration)
    elif 23 <= size < 43:
        cost = class_3_cost(distance, duration)
    elif 43 <= size < 59:
        cost = class_4_cost(distance, duration)
    elif 59 <= size < 87:
        cost = class_5_cost(distance, duration)
    else:
        raise CalculateCostError("Should be less then 86m3. Create 2 orders.")

    return convert_coins_to_uah(cost)


def calculate_size(length, width, height):
    return float(length) * float(width) * float(height)


def convert_centimeter_to_meter(l):
    return float(l)/100


def convert_meter_to_centimeter(l):
    return float(l)*100


def convert_hour_to_minutes(h):
    return float(h) * 60


def convert_uah_to_coins(uah_amount):
    return Decimal(str(uah_amount)) * Decimal(100)


def convert_coins_to_uah(coins_amount):
    return Decimal(str(coins_amount)) / Decimal(100)


def class_1_cost(distance, duration):  # in coins
    logger.info('class 1')
    start_fee = 11000
    hour_fee = 11000
    minimal_hours = 2
    distance_rate = convert_uah_to_coins(4)
    if distance:
        logger.info('Distance: {}, duration: {}'.format(distance, duration))
        if duration > minimal_hours:
            extra_time_rate = hour_fee * (duration - minimal_hours)
            return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate) + extra_time_rate
        return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate)
    else:
        return start_fee + hour_fee * minimal_hours


def class_2_cost(distance, duration):  # in coins
    start_fee = 15000
    hour_fee = 15000
    minimal_hours = 2
    distance_rate = convert_uah_to_coins(5)
    if distance:
        logger.info('Distance: {}, duration: {}'.format(distance, duration))
        if duration > minimal_hours:
            extra_time_rate = hour_fee * (duration - minimal_hours)
            return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate) + extra_time_rate
        return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate)
    else:
        return start_fee + hour_fee * minimal_hours


def class_3_cost(distance, duration):  # in coins
    start_fee = 20000
    hour_fee = 20000
    minimal_hours = 3
    distance_rate = convert_uah_to_coins(7)
    if distance:
        logger.info('Distance: {}, duration: {}'.format(distance, duration))
        if duration > minimal_hours:
            extra_time_rate = hour_fee * (duration - minimal_hours)
            return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate) + extra_time_rate
        return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate)
    else:
        return start_fee + hour_fee * minimal_hours


def class_4_cost(distance, duration):  # in coins
    start_fee = 27000
    hour_fee = 27000
    minimal_hours = 4
    distance_rate = convert_uah_to_coins(15)
    if distance:
        logger.info('Distance: {}, duration: {}'.format(distance, duration))
        if duration > minimal_hours:
            extra_time_rate = hour_fee * (duration - minimal_hours)
            return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate) + extra_time_rate
        return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate)
    else:
        return start_fee + hour_fee * minimal_hours


def class_5_cost(distance, duration):  # in coins
    start_fee = 43000
    hour_fee = 43000
    minimal_hours = 4
    distance_rate = convert_uah_to_coins(20)
    if distance:
        logger.info('Distance: {}, duration: {}'.format(distance, duration))
        if duration > minimal_hours:
            extra_time_rate = hour_fee * (duration - minimal_hours)
            return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate) + extra_time_rate
        return start_fee + hour_fee * minimal_hours + float(distance) * 2 * float(distance_rate)
    else:
        return start_fee + hour_fee * minimal_hours


def get_distance(from_address, to_address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
    result = gmaps.distance_matrix(from_address, to_address, language='ru-RU', mode='driving')
    distance = float(result['rows'][0]['elements'][0]['distance']['value']) / 1000  # in km
    duration = float(result['rows'][0]['elements'][0]['duration']['value']) / 3600  # in hours
    return distance, duration
