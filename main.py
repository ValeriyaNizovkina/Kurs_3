import os
from operator import itemgetter
from utils import get_operations, filter_by_state, templ_operation

# Получаем полный путь к файлу с данными
OPERATION_DIR = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(OPERATION_DIR, 'operations.json')
# Получаем данные по операциям
user_operations = get_operations(data_file)
# Фильтруем данные - отбираем только EXECUTED операции
user_exec = filter_by_state(user_operations, 'EXECUTED')

# Сортируем данные по дате и получаем последние 5 операций
# Для каждой операции получаем отформатированные данные и выводим их на экран
for i in sorted(user_exec, key=itemgetter('date'), reverse=True)[:5]:
    data, descr, source, destin, amount, currency = templ_operation(i)
    print(data, descr)
    print(source, '->', destin) if source else print(destin)
    print(amount, currency, "\n")
