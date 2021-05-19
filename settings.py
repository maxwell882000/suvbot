import shelve
from config import basedir
import os
from typing import Optional, Tuple

filename = os.path.join(basedir, 'settings')


def get_delivery_cost() -> tuple:
    """
    Get delivery cost
    :return: (First 3 km, and longer)
    """
    settings = shelve.open(filename)
    if 'delivery_cost' not in settings:
        settings['delivery_cost'] = (3000, 1000)
    value = settings['delivery_cost']
    settings.close()
    return value


def set_delivery_cost(prices: tuple):
    """
    Set delivary prices
    :param prices: (First 3 km, and longer)
    :return: void
    """
    settings = shelve.open(filename)
    settings['delivery_cost'] = prices
    settings.close()


def get_cafe_coordinates() -> Optional[Tuple[float, float]]:
    """
    Cafe coordinates
    :return: (latitude, longitude)
    """
    settings = shelve.open(filename)
    if 'cafe_coordinates' not in settings:
        return None
    value = settings['cafe_coordinates']
    settings.close()
    return value


def set_cafe_coordinates(coordinates: tuple):
    """
    Set cafe coordinates
    :param coordinates: (latitude, longitude)
    :return: void
    """
    settings = shelve.open(filename)
    settings['cafe_coordinates'] = coordinates
    settings.close()


def set_limit_delivery_price(price: int):
    """
    Set limit delivery cost
    :param price: price value
    :return: void
    """
    settings = shelve.open(filename)
    settings['limit_delivery_price'] = price
    settings.close()


def get_limit_delivery_price() -> int:
    """
    Get limit delivery cost or set default value - 15000
    :return: limit delivery price
    """
    settings = shelve.open(filename)
    if 'limit_delivery_price' not in settings:
        settings['limit_delivery_price'] = 15000
    value = settings['limit_delivery_price']
    settings.close()
    return value


def set_limit_delivery_km(price: int):
    """
    Set limit delivery cost
    :param price: price value
    :return: void
    """
    settings = shelve.open(filename)
    settings['limit_delivery_km'] = price
    settings.close()


def get_limit_delivery_km() -> int:
    """
    Get limit delivery cost or set default value - 15000
    :return: limit delivery price
    """
    settings = shelve.open(filename)
    if 'limit_delivery_km' not in settings:
        settings['limit_delivery_km'] = 15
    value = settings['limit_delivery_km']
    settings.close()
    return value


def set_currency_value(value: int):
    """
    Set currency value
    :param value: currency value
    :return: void
    """
    settings = shelve.open(filename)
    settings['currency_value'] = value
    settings.close()


def get_currency_value() -> int:
    """
    Get currency value
    :return: currency value
    """
    settings = shelve.open(filename)
    if 'currency_value' not in settings:
        settings['currency_value'] = 10200
    value = settings['currency_value']
    settings.close()
    return value


def set_about_text(text: str):
    """
    Set about text
    :return: void
    """
    settings = shelve.open(filename)
    settings['about_text_ru'] = text
    settings.close()


def set_about_text_uz(text: str):
    """
    Set about text on Uzbek
    :return: void
    """
    settings = shelve.open(filename)
    settings['about_text_uz'] = text
    settings.close()


def get_about_text(language) -> str:
    """
    Get about text
    :return: about text
    """
    settings = shelve.open(filename)
    if language == 'uz':
        if 'about_text_uz' not in settings:
            settings['about_text_uz'] = 'Salom! Biz kompaniya va biz sotamiz!'
        value = settings['about_text_uz']
        settings.close()
        return value
    else:
        if 'about_text_ru' not in settings:
            settings['about_text_ru'] = 'Привет! Мы КОМПАНИЯ и мы ПРОДАЁМ!'
        value = settings['about_text_ru']
        settings.close()
        return value
