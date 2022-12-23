def conv_to_float(string):
    try:
        return float(string)
    except ValueError:
        if string == '':
            return 0
        else:
            return string


def partition(dicts, key, low, high):
    pivot = conv_to_float(dicts[(low + high) // 2][key])
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while conv_to_float(dicts[i][key]) < pivot:
            i += 1

        j -= 1
        while conv_to_float(dicts[j][key]) > pivot:
            j -= 1

        if i >= j:
            return j

        dicts[i], dicts[j] = dicts[j], dicts[i]


def _dicts_quick_sort(in_data, key, low, high):
    if low < high:
        split_index = partition(in_data, key, low, high)
        _dicts_quick_sort(in_data, key, low, split_index)
        _dicts_quick_sort(in_data, key, split_index + 1, high)


def dicts_quick_sort(in_data, key):
    _dicts_quick_sort(in_data, key, 0, len(in_data) - 1)


def additional_sort(in_data, curr_key, prev_key):
    prev_key_buffer = in_data[0][prev_key]
    low = 0
    high = 0
    for _dict in in_data[1:]:
        high += 1
        if _dict[prev_key] != prev_key_buffer:
            if high-low > 1:
                _dicts_quick_sort(in_data, curr_key, low, high-1)

            low = high
            prev_key_buffer = _dict[prev_key]


