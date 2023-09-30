from e_commerce.gen_fake_data import get_fake_data


def test_get_fake_data():
    data1 = get_fake_data()
    data2 = get_fake_data()
    assert data1 != data2


def test_len_fake_data():
    data = get_fake_data()
    assert len(data) == 5


def test_valid_keys_fake_data():
    data = get_fake_data()
    expected_keys = ["name", "address", "email", "phone_number", "country"]
    assert sorted(data.keys()) == sorted(expected_keys)
