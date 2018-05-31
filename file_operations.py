import os
import enum

class SEARCH_TYPE(enum.Enum):
    LINEAR = 0
    PARALLEL = 1

def search_from_file(filename, search_term,search_type):
    '''Handle the process of searching for data in a file'''
    with open(filename, "r") as searchfile:
        # returns full line of first instance of search term
        if ( search_type == SEARCH_TYPE.LINEAR.value ):
            for line in searchfile:
                if search_term in line:
                    return line.rstrip()
        elif ( search_type == SEARCH_TYPE.PARALLEL.value ):
            # returns dictionary of all lines of search term
            file_lines = {}
            for num, line in enumerate(searchfile, 0):
                if search_term in line:
                    file_lines[num] = line.rstrip()
            return file_lines if any(file_lines.values()) else None

def read_from_file(filename):
    '''Handle the process of reading data from a file'''
    file_lines = dict()
    with open(filename, "r") as readfile:
        for num, line in enumerate(readfile, 0):
            file_lines[num] = line.rstrip()
        return file_lines

def update_file(filename, update_term, write_value):
    '''Handle the process of updating data in a file'''

    data = update_term + "," + write_value

    with open(filename + ".tmp", "w") as outFile:

        with open(filename, "r") as inputfile:
            for line in inputfile:

                if update_term in line:
                    outFile.writelines("{}\n".format(data.rstrip()))
                else:
                    outFile.writelines("{}\n".format(line.rstrip()))
    os.rename(filename + ".tmp", filename)


def write_to_file(filename, data):
    '''Handle the process of writing data to a file'''
    with open(filename, "a") as file:
        file.writelines("{}\n".format(data))
