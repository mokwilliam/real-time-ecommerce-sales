from typing import List, Union

import pandas as pd
from gen_fake_data import get_fake_data


def process_data(data: Union[dict, List[dict]]):  # -> Union[dict, List[dict]]:
    # TODO: This function transforms the data and saves it to a database
    # transform_data(data)
    # save_data(data)
    pass


def transform_data(data: Union[dict, List[dict]]):
    df = pd.DataFrame(data)
    if type(data) is dict:
        print("dict")
    elif type(data) is list:
        print("list")
    else:
        raise TypeError("Invalid data type")
    pass


if __name__ == "__main__":
    data = [get_fake_data() for _ in range(10)]
    # process_data(data)
