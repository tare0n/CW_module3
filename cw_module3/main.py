import csv
from csv_sort import *
from dict_sort import dicts_quick_sort

sorting_keys = {1: "открытия",
                2: "закрытия",
                3: "максимум",
                4: "минимум",
                5: "объем"}
header = ["date", "open", "close", "high", "low", "volume"]


def open_csv(filename):
    with open(filename, newline='') as csvfile:
        data = [{key: value for key, value in row.items()}
                for row in csv.DictReader(csvfile, skipinitialspace=True)]
    return data


def get_sorted():

    print("Сортировать по цене:/n")
    for key in sorting_keys.keys():
        if key != 3:
            print(f"{sorting_keys[key]} ({key})")
        else:
            print(f"{sorting_keys[key]} [{key}]")

    sorting_key = input()
    if sorting_key not in sorting_keys.keys():
        sorting_key = 3
    column = header[sorting_key]

    order_key = input("Порядок по убыванию [1] / возрастанию (2):")
    if order_key not in [1, 2]:
        order_key = 1
    if order_key == 1:
        order = 'desc'
    else:
        order = 'asc'

    limit = input("Ограничение выборки [10]:")
    if not isinstance(limit, int):
        try:
            limit = int(limit)
        except TypeError:
            limit = 10

    filename = input("Название файла для сохранения результата [dump.csv]: ")
    if "." not in filename:
        filename = "dump.csv"

    select_sorted(open_csv("all_stocks_5yr.csv"), [column], limit, order, filename)


def get_banch():
    date = input("Дата в формате yyyy-mm-dd [all]: ")
    if len(date) != 10:
        date = 'all'
    name = input("Тикер [all]: ")
    if len(name) < 3 or len(name) > 7:
        name = 'all'
    filename = input("Файл [dump.csv]: ")
    if "." not in filename:
        filename = 'dump.csv'

    in_data = open_csv('all_stocks_5yr.csv')
    #dicts_quick_sort(in_data, 'Name')
    if date == 'all':

        if name == 'all':
            with open(filename, 'w', newline='') as dump:
                field_names = in_data.keys()
                writer = csv.DictWriter(dump, fieldnames=field_names)
                writer.writeheader()
                for row in in_data:
                    writer.writerow(row)

        else:
            get_by_name_only(in_data, name, filename)

    else:
        if name == "all":
            for i in in_data[:20]:
                print(f"date: {i['date']} name: {i['Name']}")
            dicts_quick_sort(in_data, 'date')
            for i in in_data[:20]:
                print(f"date: {i['date']} name: {i['Name']}")
            get_by_date_only(in_data, date, filename)
        else:
            get_by_date(in_data, date, name, filename)


get_banch()