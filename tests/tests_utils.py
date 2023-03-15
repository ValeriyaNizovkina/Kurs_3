import json
import pytest

import utils
import main


@pytest.fixture
def test_data():
    with open(main.data_file, 'rt', encoding='utf-8') as data_file:
        return json.loads("".join(data_file.readlines()))


@pytest.fixture
def test_data_ok():
    result = []
    with open(main.data_file, 'rt', encoding='utf-8') as data_file:
        for item in json.loads("".join(data_file.readlines())):
            if item:
                result.append(item)
    return result


@pytest.fixture
def test_6_items():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {
                "amount": "48223.05",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
    ]


def test_get_operations(test_data):
    assert utils.get_operations(main.data_file) != test_data


def test_filter_by_state(test_data_ok):
    for item in utils.filter_by_state(test_data_ok, 'EXECUTED'):
        assert item['state'] == 'EXECUTED'

    for item in utils.filter_by_state(test_data_ok, 'CANCELED'):
        assert item['state'] == 'CANCELED'

    assert utils.filter_by_state(test_data_ok, 'TEST') == []


def test_templ_operation(test_6_items):
    data, descr, source, destin, amount, currency = utils.templ_operation(test_6_items[0])
    assert data == '26.08.2019'
    assert descr == "Перевод организации"
    assert source == "Maestro 1596 83** **** 5199"
    assert destin == "Счет **9589"
    assert amount == "31957.58"
    assert currency == "руб."
    data, descr, source, destin, amount, currency = utils.templ_operation(test_6_items[2])
    assert data == '30.06.2018'
    assert descr == "Перевод организации"
    assert source == "Счет **6952"
    assert destin == "Счет **6702"
    assert amount == "9824.07"
    assert currency == "USD"


def test_format_date():
    assert utils.format_date("2019-08-26T10:50:58.294041") == "26.08.2019"
    assert utils.format_date("2019-07-03T18:35:29.512364") == "03.07.2019"
    assert utils.format_date("2018-06-30T02:08:58.425572") == "30.06.2018"


def test_add_mask():
    assert utils.add_mask("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
    assert utils.add_mask("Счет 64686473678894779589") == "Счет **9589"
    assert utils.add_mask("Счет 646864736788") == 'Счет ???_номер_карты,_счёта_???'
