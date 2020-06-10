import os
from matplotlib.pyplot import show
from matplotlib.pyplot import scatter
from matplotlib.pyplot import title
import numpy


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


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        pass


def convert_to_specific_format(number):
    """
    Convert index (ancestor) to a specific format presented
    in point "Compression representation"
    :param number: index (ancestor)
    :return:
    """
    if number<=127:
        return '1'+"{0:08b}".format(number)[1:]
    else:
        str=("{0:08b}".format(number))
        zeroes = (get_next_multiple_7(len(str)) - len(str))
        prefix = "".join(["0" for i in range(zeroes)])
        temp=prefix+str
        temp_2=''
        for i in range(0,len(temp),7):
            if i+7==len(temp):
                temp_2 = temp_2 + '1' + temp[i:i + 7]
            else:
                temp_2 = temp_2 + '0' + temp[i:i + 7]

        return temp_2


def get_next_multiple_7(num):
    temp=0
    while(temp < num):
        temp=temp+7
    return temp


def encode(file_input_path, file_output_path):
    dictionary = {}
    file_input=open(file_input_path, 'rb')

    file = file_input.read()

    result = []
    index = 0
    temp=''
    for i in range(len(file)):
        temp = temp+"{0:08b}".format(file[i])
        if temp not in dictionary:
            index = index+1
            if len(temp)==8:
                dictionary[temp]=(index,0, temp)
            else:
                dictionary[temp]=(index,dictionary[temp[0:len(temp)-8]][0],temp[len(temp)-8:len(temp)])
            result.append((convert_to_specific_format(dictionary[temp][1]) + dictionary[temp][2]))
            temp = ''
        elif i==len(file)-1:

            result.append((convert_to_specific_format(dictionary[temp][1]) + dictionary[temp][2]))
            temp = ''



    result="".join(result)

    file_output = open(file_output_path, 'wb')
    for i in range(0,len(result),8):
        file_output.write(bytes([int(result[i:i+8], base=2)]))
    file_input.close()
    file_output.close()

def decode(file_input_path, file_output_path):
    temp = []
    file_input=open(file_input_path, 'rb')
    line = file_input.read()
    end = '0'
    index=''
    for i in line:
        if end=='0':
            bits = "{0:08b}".format(i)
            end=bits[0]
            index = index + bits[1:8]
        else:
            symbol="{0:08b}".format(i)
            end = '0'
            index = int(index, base=2)
            temp.append((index, symbol))
            index=''
    file_output=open(file_output_path, 'wb')
    for i in range(len(temp)):
        result = ''
        result = temp[i][1] + result
        index=temp[i][0]
        while(index!=0):
            result = temp[index-1][1] + result
            index = temp[index-1][0]

        for j in range(0, len(result), 8):
            file_output.write(bytes([int(result[j:j+8], base=2)]))

    file_input.close()
    file_output.close()

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

paths= next(os.walk("dataset"))[1]
create_dir("DariaVaskovskayaOutputs")
dict_plot = {}
for i in paths:
    create_dir("DariaVaskovskayaOutputs"+"/"+i)
for i in paths:
    size_compressed = 0
    size = 0
    files = [i.split('/')[-1] for i in return_files_in_dir("dataset"+"/"+i)]
    list_x = []
    list_y = []
    for filename in files:
        src = "dataset" +"/" + i + "/" + filename
        dest = "DariaVaskovskayaOutputs" +'/' + i + '/'+ filename.split(".")[0] + "Decompressed" + "."+ filename.split(".")[1]
        path_to_compressed="DariaVaskovskayaOutputs" +'/' + i + '/'+ filename.split(".")[0] + "Compressed" + "."+ filename.split(".")[1]
        print("Processing",path_to_compressed)
        encode(src, path_to_compressed)
        decode(path_to_compressed,dest)
        size_compressed = size_compressed + get_size(path_to_compressed)
        size=size + get_size(dest)
        compressed_size=get_size(path_to_compressed)
        initial_size = get_size(dest)
        compression_ratio= initial_size/ compressed_size
        list_x.append(initial_size)
        list_y.append(compression_ratio)
    dict_plot[i] = list_x, list_y

    print("Average compression ratio for", i, size/size_compressed)



for i in dict_plot.items():
    list_x = i[1][0]
    list_y = i[1][1]
    print("Correlation:")
    print(i[0], numpy.corrcoef(list_x, list_y)[0, 1])
    scatter(list_x, list_y)
    title(i[0])
    show()






show()



(encode("mem-yaytso.jpg", "test_output.jpg"))
decode("test_output.jpg", "decode_output.jpg")









