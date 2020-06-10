import os
from cmath import exp
from matplotlib import pyplot
from matplotlib import numpy as np


def FFT(x):
    """
    A recursive implementation of FFT
    :param x: 1D numpy array
    :return: 1D numpy array
    """
    N = len(x)
    if N <= 1: return x
    even = FFT(x[0::2])
    odd =  FFT(x[1::2])
    T= [exp(-2j*np.pi*k/N)*odd[k] for k in range(N//2)]
    return np.array([even[k] + T[k] for k in range(N//2)] + \
           [even[k] - T[k] for k in range(N//2)])

def iFFT(x):
    """
    A recursive implementation of inverse FFT
    :param x: 1D numpy array
    :return: 1D numpy array
    """
    N = len(x)
    return np.array(iFFT_impl(x))/N

def iFFT_impl(x):
    """
    A helper function for a recursive implementation of inverse FFT
    :param x: 1D numpy array
    :return:1D numpy array
    """
    N = len(x)
    if N <= 1: return x
    even = iFFT(x[0::2])
    odd =  iFFT(x[1::2])
    T= [exp(2j*np.pi*k/N)*odd[k] for k in range(N//2)]
    return [even[k] + T[k] for k in range(N//2)] + \
           [even[k] - T[k] for k in range(N//2)]

def FFT2D(M):
    """
    :param M: 2D matrix
    :return: 2D matrix
    """
    num_rows, num_columns = M.shape
    FFTed = np.zeros((num_rows, num_columns), dtype=complex)
    for i in range(num_columns):
        new_elem = FFT(M[:, i])
        FFTed[:, i] = new_elem
    finally_FFTed = np.zeros((num_rows, num_columns), dtype=complex)
    for i in range(num_rows):
        new_elem = FFT(FFTed[i])
        finally_FFTed[i] = new_elem
    return finally_FFTed

def cutoff(AT):
    """
    Compression function
    :param AT: matrix
    :return: matrix
    """
    num_rows, num_columns = AT.shape
    get_abs = np.vectorize(abs)
    magnitudes = get_abs(AT)
    threshold = np.percentile(magnitudes, 30)
    for i in range(num_rows):
        for j in range(num_columns):
            if magnitudes[i][j] < threshold:
                AT[i][j] = 0 + 0j
    return AT

def iFFT2D(AT):
    """

    :param AT: 2D matrix
    :return: 2D matrix
    """
    num_rows, num_columns = AT.shape
    FFTed = np.zeros((num_rows, num_columns), dtype=complex)
    for i in range(num_columns):
        new_elem = iFFT(AT[:, i])
        FFTed[:, i] = new_elem
    finally_FFTed = np.zeros((num_rows, num_columns), dtype=complex)
    for i in range(num_rows):
        new_elem = iFFT(FFTed[i])
        finally_FFTed[i] = new_elem
    return finally_FFTed

def return_files_in_dir(path_to_dir):
    """
    :param path_to_dir: path to the directory
    :return: list of paths to files stored in the directory which location is described by path_to_dir
    """
    files = []
    for r, d, f in os.walk(path_to_dir):
        for file in f:
            files.append(os.path.join(r, file))
    return files


def create_dir(path):
    """
    Create dir
    :param path: path to the dir which will be created
    :return:
    """
    try:
        os.mkdir(path)
    except OSError:
        pass

create_dir("DariaVaskovskayaOutputs")
files = return_files_in_dir("inputs")
for file in files:
    name = file.split("/")[1].split(".")[0]
    test = pyplot.imread(file)
    AT = FFT2D(test)
    AT = cutoff(AT)
    im  = iFFT2D(AT)
    leave_real = np.vectorize(lambda x: x.real)
    im = leave_real(im)
    name = name +"Compressed"
    pyplot.imsave("DariaVaskovskayaOutputs/" + name+ ".tif", im, cmap="gray", format="tiff")




