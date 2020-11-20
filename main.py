import os, csv
from datetime import datetime
import graphs

def main(directory):

    # first step is to check if a .csv log file exists, and if not,
    # create a new .csv file in which info obtained from the directory walk
    # will be stored
    scanDir = directory
    # if top_dir is a lettered drive, its naming convention will end in a slash. But if any other folder is chosen,
    # this isn't true. Since the log is parsed using slashes as split anchors, must account for this

    if scanDir.split('\\')[-1] == '':
        # true if passed a letter drive as top_dir
        scanName = scanDir.split(':\\')[-2]
    else:
        # true if passed any directory lower than a top letter drive
        scanName = scanDir.split('\\')[-1]

    logDir = 'D:\SYSTEM SCAN LOGS'
    os.chdir(logDir)
    logName = "MASTER SYSTEM SCAN LOG - " + scanName + ".csv"
    fullLogName = logDir + '\\' + logName

    date = datetime.now()
    scanDate = date.strftime("%b-%d-%Y __ %Hh %Mm %Ss")

    # if this is first execution of the program, we must instantiate the master log file
    for dirpath, dirnames, filenames in os.walk(logDir):
        if logName not in filenames:
            # only true on first program execution. Create .csv file and add its first header, "Directory"
            logFile = open(logName, 'x')
            logFile.write('Directory')
            logFile.close()
        break

    # walk through the given directory and check the size of both the directory, and ALL
    # subdirectories

    dirSizes = {}
    totalErrors = 0
    i = 0

    for dirpath, dirnames, filenames in os.walk(scanDir):
        # calls method which will walk through the given directory and calculate
        # total size
        size, errors = get_folder_size(dirpath)
        totalErrors += errors
        dirSizes[dirpath] = size


    # write to the CSV file
    try:
        write_to_log(dirSizes, scanDate, logName, logDir)
    except PermissionError:
        print("Scan log is open. Close it and re-run the scanner")
        return 1

    print("Scan finished with " + str(totalErrors) + " errors.")

    return fullLogName, scanDate

def get_folder_size(dir):
    # this function will iterate through all files and subdirectories of the given directory and calculate a
    # cumulative size of all the folder's contents

    # initiate size
    size = 0
    errors = 0

    for dirpath, dirnames, filenames in os.walk(dir):
        for file in filenames:
            try:
                filename = os.path.join(dirpath, file)
                size += os.stat(filename).st_size
            except OSError:
                errors += 1
                pass

    return size, errors


# two main functions: append size information to appropriate column (scandate), and add rows for new directories
def write_to_log(dirSizes, scanDate, logName, logDir):
    os.chdir(logDir)
    old_rows_list = []
    new_rows_list = []
    deleted_dirs = []
    new_dirs = []

    # first, read all current data of log into memory
    with open(logName, 'r') as logFile:
        reader = csv.reader(logFile)
        for row in reader:
            new_row = ""
            for item in row:
                new_row += str(item + ',')
            old_rows_list.append(new_row)

    # then, write old rows plus new scan data back into the csv file, by appending new scan data
    # to the rows in old_rows_list
    for row in old_rows_list:
        # if current directory in old_rows exists, append data to the end of it from dirSizes dict
        curDir = row.split(",")[0]
        # append new scan date as new column header to first row
        if curDir == 'Directory':
            row += str(scanDate)
            new_rows_list.append(row)

            # count number of commas in header to determine how many scans have happened
            scanCount = count_scans(row)

        # append new size data to corresponding directory row
        elif curDir in dirSizes.keys() and curDir != "Directory":
            row += str(dirSizes[curDir])
            new_rows_list.append(row)
            # now that the key has been referenced, we don't need it anymore
            # we want to use any leftover keys for next phase
            del dirSizes[curDir]
        # if directory is not in dirSizes dict, that means it's been removed
        else:
            deleted_dirs.append(curDir)

    # undeleted key pairs in dirSizes represent NEW directories that have been added since last scan
    # must add as many commas to row as number of past scans, to ensure the data ends up in the appropriate column
    for key, value in dirSizes.items():
        new_rows_list.append(str(key) + (scanCount * ",") + str(value))
        new_dirs.append(key)

    #print("new dirs:", new_dirs)
    #print("deleted dirs:", deleted_dirs)

    # write data into csv
    with open(logName, 'w') as logFile:
        for item in new_rows_list:
            try:
                logFile.write(item + '\n')
            except UnicodeError:
                pass


def count_scans(row):
    scanCount = 0
    for i in row:
        if i == ',':
            scanCount += 1

    return scanCount


# main('D:\Game Making')

