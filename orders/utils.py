from decimal import Decimal


class CalculateCostError(Exception):
    def __init__(self, message):
        self.message = message


def get_order_cost(data):
    size = calculate_size(data.get('length'), data.get('width'), data.get('height'))

    if size < 9:
        cost = class_1_cost()
    elif 9 <= size < 23:
        cost = class_2_cost()
    elif 23 <= size < 43:
        cost = class_3_cost()
    elif 43 <= size < 59:
        cost = class_4_cost()
    elif 59 <= size < 87:
        cost = class_5_cost()
    else:
        raise CalculateCostError('Size more than 68 m3')
    return convert_coins_to_uah(cost)


def calculate_size(length, width, height):
    return float(length) * float(width) * float(height)


def convert_centimeter_to_meter(l):
    return float(l)/100


def convert_meter_to_centimeter(l):
    return float(l)*100


def convert_uah_to_coins(uah_amount):
    return Decimal(str(uah_amount)) * Decimal(100)


def convert_coins_to_uah(coins_amount):
    return Decimal(str(coins_amount)) / Decimal(100)


def class_1_cost():  # in coins
    start_fee = 11000
    hour_fee = 11000
    minimal_hours = 2
    return start_fee + hour_fee * minimal_hours


def class_2_cost():  # in coins
    start_fee = 15000
    hour_fee = 15000
    minimal_hours = 2
    return start_fee + hour_fee * minimal_hours


def class_3_cost():  # in coins
    start_fee = 20000
    hour_fee = 20000
    minimal_hours = 3
    return start_fee + hour_fee * minimal_hours


def class_4_cost():  # in coins
    start_fee = 27000
    hour_fee = 27000
    minimal_hours = 4
    return start_fee + hour_fee * minimal_hours


def class_5_cost():  # in coins
    start_fee = 43000
    hour_fee = 43000
    minimal_hours = 4
    return start_fee + hour_fee * minimal_hours
