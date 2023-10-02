import datetime
from random import randint
from typing import List

from faker import Faker

LOCATION_LIST = [
    # "it_IT",
    "en_GB",
    # "fr_FR",
    # "es_ES",
    # "de_DE",
    # "pl_PL",
    # "pt_PT",
    # "nl_NL",
]

RANDOM_OBJECT_LIST = [
    "lamp",
    "chair",
    "table",
    "sofa",
    "bed",
    "coat",
    "sweater",
    "skirt",
    "dress",
    "shirt",
    "shoe",
    "bag",
    "scarf",
    "glove",
    "hat",
    "jacket",
    "jeans",
    "shorts",
]


def get_fake_customer(faker) -> dict:
    """Gets fake customer data.

    Returns:
        dict: A dictionary containing fake customer data.
    """
    return {
        "name": faker.name(),
        "address": faker.address(),
        "email": faker.email(),
        "phone_number": faker.phone_number(),
        "country": faker.country(),
    }


def get_fake_product() -> dict:
    """Gets fake product data.

    Returns:
        dict: A dictionary containing fake product data.
    """
    # Get one location among the list
    # local = LOCATION_LIST[randint(0, len(LOCATION_LIST) - 1)]
    local = "en_GB"
    faker = Faker([local])
    return {
        "name": faker.word(ext_word_list=RANDOM_OBJECT_LIST),
        "price": faker.pyfloat(min_value=10, max_value=100, right_digits=2),
        "description": faker.text(),
    }


def get_fake_order(faker) -> dict:
    """Gets fake order data.

    Returns:
        dict: A dictionary containing fake order data.
    """
    return {
        "order_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "quantity": faker.pyint(min_value=1, max_value=5),
        "product": faker.word(ext_word_list=RANDOM_OBJECT_LIST),
    }


def get_fake_data() -> List[dict]:
    """Gets fake data.

    Returns:
        List[dict]: A list of dictionaries containing fake data.
    """
    # Get one location among the list
    # local = LOCATION_LIST[randint(0, len(LOCATION_LIST) - 1)]
    local = "en_GB"
    faker = Faker([local])
    order = get_fake_order(faker)
    customer = get_fake_customer(faker)
    return customer, order
