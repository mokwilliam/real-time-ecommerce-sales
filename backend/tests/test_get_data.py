from e_commerce.gen_fake_data import get_fake_data, get_fake_product


def test_get_fake_data():
    data1 = get_fake_data()
    data2 = get_fake_data()
    assert data1 != data2


def test_len_product():
    product = get_fake_product()
    assert len(product) == 3


def test_len_customer():
    customer, _ = get_fake_data()
    assert len(customer) == 5


def test_len_order():
    _, order = get_fake_data()
    assert len(order) == 3


def test_valid_keys_fake_product():
    product = get_fake_product()
    expected_keys = ["name", "price", "description"]
    assert sorted(product.keys()) == sorted(expected_keys)


def test_valid_keys_fake_customer():
    customer, _ = get_fake_data()
    expected_keys = ["name", "address", "email", "phone_number", "country"]
    assert sorted(customer.keys()) == sorted(expected_keys)


def test_valid_keys_fake_order():
    _, order = get_fake_data()
    expected_keys = ["order_date", "quantity", "product"]
    assert sorted(order.keys()) == sorted(expected_keys)
