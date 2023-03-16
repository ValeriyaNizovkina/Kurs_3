import json
from datetime import datetime


def get_operations(path_file: str):
    """
    Функция получает данные из файла operations.json в корне проекта и отбрасывает пустые словари
    :return: Список операций в виде списка словарей
    """
    result = []
    with open(path_file, 'rt', encoding='utf-8') as data_file:
        for item in json.loads("".join(data_file.readlines())):
            if item:
                result.append(item)
    return result


def filter_by_state(data_list: list, st_val: str) -> list:
    """
    Функция возвращает отфильтрованный список по ключу 'state'
    :param data_list: Исходный список
    :param st_val: Значение ключа 'state' для фильтра
    :return: Отфильтрованный список операций
    """
    result = []
    for item_dict in data_list:
        if item_dict['state'] == st_val:
            result.append(item_dict)
    return result


def templ_operation(oper_dict: dict):
    """
    Функция получает словарь с данными операции и возвращает отформатированные данные для вывода
    :param oper_dict: словарь с данными по операции
    :return: отформатированные данные по операции - дата, описание, источник, назначение, сумма и валюта операции
    """
    data_op = format_date(oper_dict.get('date'))
    descr_op = oper_dict.get('description')
    source_op = add_mask(oper_dict.get('from')) if oper_dict.get('from') else ''
    destin_op = add_mask(oper_dict.get('to'))
    amount_op = oper_dict.get('operationAmount', {}).get('amount')
    currency_op = oper_dict.get('operationAmount', {}).get('currency', {}).get('name')
    return data_op, descr_op, source_op, destin_op, amount_op, currency_op


def format_date(date: str) -> str:
    """
    Функция конвертирует строку даты в дату, форматирует и возвращает в виде строки
    :param date: строка с датой YYYY-MM-DD*
    :return: строка с отформатированной датой dd.mm.yyyy
    """
    date_type = datetime.strptime(date[:10], "%Y-%m-%d")
    result = date_type.strftime("%d.%m.%Y")
    return result


def add_mask(original_str: str):
    """
    Функция возвращает замаскированный номер счета или номер карты.
    Если длина номера не 16 и не 20, номер маскируется целиком.
    :param original_str: Исходная строка с номером счёта или карты
    :return: Исходная строка с замаскированным номером
    """
    original_lst = original_str.split()
    if len(original_lst[-1]) == 20:
        original_lst[-1] = '**' + original_lst[-1][-4:]
    elif len(original_lst[-1]) == 16:
        original_lst[-1] = f'{original_lst[-1][:4]} {original_lst[-1][4:6]}** **** {original_lst[-1][-4:]}'
    else:
        original_lst[-1] = '???_номер_карты,_счёта_???'
    return " ".join(original_lst)
