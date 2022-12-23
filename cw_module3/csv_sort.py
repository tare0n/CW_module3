import csv
from dict_sort import dicts_quick_sort, additional_sort

cache_dictionary = {}


def cache(cache_dict):
    def _cache(func):
        def inner(*args):
            key_string = "___"
            for arg in args[1:]:
                key_string += f"{arg}_"
            if key_string in cache_dict.keys():
                return cache_dict[key_string]
            else:
                out_data = func(*args)
                cache_dict[key_string] = out_data
                return out_data

        return inner
    return _cache


def select_sorted(in_data, sort_columns=["high"], limit=30, order='desc', filename='dump.csv'):
    """
    sorts values of all_stocks_5yr.csv
    :param in_data: dict with data from all_stocks_5yr.csv or other file
    :param sort_columns: columns for sorting
    :param limit: limit of highest/lowest values in result
    :param order: 'desc' for descending sort, 'asc' for ascending sort
    :param filename: file for sorted data
    :return: None
    """
    out_data = dict_select(in_data, sort_columns, limit, order)
    with open(filename, 'w', newline='') as dump:
        field_names = out_data[0].keys()
        writer = csv.DictWriter(dump, fieldnames=field_names)
        writer.writeheader()
        for coll in out_data:
            writer.writerow(coll)


@cache(cache_dictionary)
def dict_select(in_data, sort_columns, limit=619040, order='asc'):
    dicts_quick_sort(in_data, sort_columns[0])
    for i in range(1, len(sort_columns)):
        additional_sort(in_data, sort_columns[i], sort_columns[i-1])
    if order == 'desc':
        out_data = in_data[-limit:][::-1]
    elif order == 'asc':
        out_data = in_data[:limit]
    else:
        raise Exception("Incorrect order")
    return out_data


def get_by_date(in_data, date="2017-08-08", name="PCLN", filename='dump.csv'):
    left = 0
    right = len(in_data)
    mid = (left+right)//2
    while in_data[mid]['Name'] != name:
        if in_data[mid]['Name'] < name:
            left = mid
            mid = (left+right)//2
        else:
            right = mid
            mid = (left+right)//2
        if right-left < 1:
            raise Exception("Name not found")
    residue = right-left
    while in_data[mid]['date'] != date:
        if in_data[mid]['date'] > date:
            mid -= residue
        else:
            mid += residue
            residue //= 2
        if residue < 1:
            raise Exception("date not found")
    out_data = in_data[mid]
    with open(filename, 'w', newline='') as dump:
        field_names = out_data.keys()
        writer = csv.DictWriter(dump, fieldnames=field_names)
        writer.writeheader()
        writer.writerow(out_data)


def get_by_date_only(in_data, date="2017-08-08", filename='dump.csv'):
    left = 0
    right = len(in_data)
    mid = (left + right) // 2
    residue = mid // 2
    while in_data[mid]['date'] == in_data[mid-1]['date'] or in_data[mid]['date'] != date:
        if in_data[mid]['date'] >= date and mid >= residue:
            mid -= residue
        else:
            mid += residue
            residue //= 2
        if residue < 1:
            break

    out_data = []
    while in_data[mid]['date'] == date:
        out_data.append(in_data[mid])
        mid += 1

    with open(filename, 'w', newline='') as dump:
        field_names = out_data[0].keys()
        writer = csv.DictWriter(dump, fieldnames=field_names)
        writer.writeheader()
        for coll in out_data:
            writer.writerow(coll)


def get_by_name_only(in_data, name="PCLN", filename='dump.csv'):
    left = 0
    right = len(in_data)
    mid = (left + right) // 2
    residue = mid // 2
    while in_data[mid]['Name'] == in_data[mid - 1]['Name'] or in_data[mid]['Name'] != name:
        if in_data[mid]['Name'] > name:
            mid -= residue
        else:
            mid += residue
            residue //= 2

    out_data = []
    while in_data[mid]['Name'] == name:
        out_data.append(in_data[mid])
        mid += 1

    with open(filename, 'w', newline='') as dump:
        field_names = out_data[0].keys()
        writer = csv.DictWriter(dump, fieldnames=field_names)
        writer.writeheader()
        for coll in out_data:
            writer.writerow(coll)

