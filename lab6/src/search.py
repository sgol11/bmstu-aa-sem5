def sort_dict(my_dict):
    keys = list(my_dict.keys())
    keys.sort()

    tmp_dict = dict()

    for key in keys:
        tmp_dict[key] = my_dict[key]

    return tmp_dict


def binary_search(sort_dict, find_key, output=True):
    count = 0
    result = -1

    keys = list(sort_dict.keys())

    left = 0
    right = len(keys) - 1
    middle = len(keys) // 2
    while left <= right:
        count += 1

        key = keys[middle]
        if key == find_key:
            if output:
                print(list(sort_dict.items())[middle])
            result = 0
            break

        elif key < find_key:
            left = middle + 1
        else:
            right = middle - 1
        middle = (left + right) // 2

    if result == -1:
        count = -1

    return count


def process_binary_search(global_dict, find_key):
    sorted_dict = sort_dict(global_dict)
    result = binary_search(sorted_dict, find_key)
    if result == -1:
        print("Ключ не был обнаружен")


def load_csv(filename):
    file = open(filename, encoding='utf-8', newline='')

    data = []
    for line in file.readlines():
        tmp = line.replace("\r", ",").split(",")
        data.append(tmp)

    file.close()

    global_dict = {}
    for i in range(len(data)):
        key = data[i][0]
        value = data[i][1]

        global_dict[key] = value

    return global_dict

