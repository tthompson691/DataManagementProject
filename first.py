import os, pprint, csv
from datetime import datetime


def main():

    # first step is to create a new .csv file in which info obtained from the directory walk
    # will be stored
    scanDate = datetime.now()
    scanFile = scanDate.strftime("%b-%d-%Y __ %H h %M m %S s")
    os.chdir('D:\SYSTEM SCAN LOGS')
    logFile = open(scanFile + ".csv", 'x')

    logFile.write(str('DATE SCANNED: ' + str(scanDate) + '\n'))

    # walk through the given directory and check the size of both the directory, and ALL
    # subdirectories
    for dirpath, dirnames, filenames in os.walk('D:\Music\Proyectos'):

        os.chdir(dirpath)

        # calls method which will walk through the given directory and calculate
        # total size
        size = get_folder_size(dirpath)

        # write to the CSV file
        logFile.write(str(dirpath + ', ' + str(size) + '\n'))

        # for file in filenames:
        #     print(str(file) + ' is ' + str(os.stat(file).st_size) + ' bytes and was last modified on ' +
        #           str(datetime.fromtimestamp(os.stat(file).st_mtime)) + '\n')


def get_folder_size(dir):
    # this function will iterate through all files and subdirectories of the given directory and calculate a
    # cumulative size of all the folder's contents

    # initiate size
    size = 0

    for dirpath, dirnames, filenames in os.walk(dir):
        os.chdir(dirpath)

        for file in filenames:
            size += os.stat(file).st_size

    return size

def compare_data(oldLog, newLog):
    # this function compares the new scan Log to the old Log to determine if, and how much, memory space has changed
    # within each directory
    # both arguments should be filenames of the logs

    # use the .csv library to create dictionary objects out of files and read thru them
    oldReader = csv.DictReader(oldLog)
    newReader = csv.DictReader(newLog)




main()
