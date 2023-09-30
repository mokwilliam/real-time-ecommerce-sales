from random import randint

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


def get_fake_data() -> dict:
    """Gets fake data.

    Returns:
        dict: Fake data.
    """
    # Get one location among the list
    # local = LOCATION_LIST[randint(0, len(LOCATION_LIST) - 1)]
    local = "en_GB"
    faker = Faker([local])
    return {
        "name": faker.name(),
        "address": faker.address(),
        "email": faker.email(),
        "phone_number": faker.phone_number(),
        "country": faker.country(),
    }
