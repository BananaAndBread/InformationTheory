import math
import os


def get_size(file_path):
    '''
    :param file_path: path to the file
    :return: size ( in bytes) of a file which location is described by path file_path
    '''
    file = open(file_path, 'rb')
    file.seek(0, 2)  # move the cursor to the end of the file
    size = file.tell()
    file.close()
    return size


def get_bytes_frequences(file_path):
    """

    :param file_path: path to the file
    :return: list, where for list[i]=element i is a byte representation(in decimal format) and element
    is a percentage byte frequency

    """
    size = get_size(file_path)
    freuqences = list()
    for i in range(256):
        freuqences.append(0)
    with open(file_path, "rb") as f:
        byte = "start"
        while byte:
            # Do stuff with byte.
            byte = f.read(1)
            if byte:
                freuqences[byte[0]] = freuqences[byte[0]] + 1
    for i in range(len(freuqences)):
        freuqences[i] = freuqences[i] / size

    return freuqences


def count_entropy(file_path):
    """
    :param file_path: path to the file
    :return: entropy of the file which location is described by file_path
    """
    frequencies = get_bytes_frequences(file_path)
    entropy = 0.0
    for frequency in frequencies:
        if frequency != 0:
            entropy = entropy + frequency * math.log(frequency, 2)
    return -entropy


def return_files_in_dir(path_to_dir):
    """
    :param path_to_dir: path to the directory
    :return: list of paths to files stored in the directory which location is described by path_to_dir
    """
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path_to_dir):
        for file in f:
            files.append(os.path.join(r, file))
    return files


def count_average_entropy(path_to_dir):
    """
    :param path_to_dir: path to the directory
    :return: average entropy of all files stored in the directory which location is described by path_to_dir
    """
    files = return_files_in_dir(path_to_dir)
    sum = 0
    for f in files:
        sum = sum + count_entropy(f)
    return sum / len(files)


def return_top_level_dirs(path_to_dir):
    """

    :param path_to_dir: path to the directory
    :return: list of names of only top level directories located in the directory which location is described by path_to_dir
    """
    direct = next(os.walk(path_to_dir))[1]
    return direct


def count_maximum_enthropy():
    '''

    :return: maximal entropy for that range of values [0,255]
    '''
    entropy = 0
    for i in range(256):
        entropy = entropy + 1 / 256 * math.log(1 / 256, 2)
    return -entropy


def count_variance(path_to_dir):
    '''

    :param path_to_dir: path to directory
    :return: variance in entropy for all files located in the directory which location is described by path_to_dir
    '''
    files = return_files_in_dir(path_to_dir)
    average = count_average_entropy(path_to_dir)
    varience = 0
    for f in files:
        varience += (average - count_entropy(f)) ** 2
    return varience / len(files)


results = dict()
print("Average entropy (all files) ", count_average_entropy('dataset'))
print("Maximal entropy for that range of values: ", count_maximum_enthropy())
types = return_top_level_dirs('dataset')
for type in types:
    print(type, ":")
    entropy = count_average_entropy('dataset/' + type)
    variance = count_variance('dataset/' + type)
    print("   entropy: ", entropy)
    print("   variance: ", variance)
    results[type] = [entropy, variance]

print("Sorted by entropy: ")
sorted_x = sorted(results.items(), key=lambda kv: kv[1][0])
for i in sorted_x:
    print(i[0], i[1][0])
print()
print("Sorted by variance: ")
sorted_x = sorted(results.items(), key=lambda kv: kv[1][1])
for i in sorted_x:
    print(i[0], i[1][1])
