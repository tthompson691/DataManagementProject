import os, csv
from datetime import datetime
from graphs import make_pie_chart


def main():

    # first step is to create a new .csv file in which info obtained from the directory walk
    # will be stored
    scanDate = datetime.now()
    scanFile = scanDate.strftime("%b-%d-%Y __ %H h %M m %S s")
    os.chdir('D:\SYSTEM SCAN LOGS')

    # check for an old scan log for later comparison
    oldDataFound, oldData = find_old_log('D:\SYSTEM SCAN LOGS')

    logFile = open(scanFile + ".csv", 'x')

    # create headers for .csv file
    logFile.write('ScanDate,Directory,Size\n')

    # walk through the given directory and check the size of both the directory, and ALL
    # subdirectories
    for dirpath, dirnames, filenames in os.walk('D:\Music\Proyectos'):

        os.chdir(dirpath)

        # calls method which will walk through the given directory and calculate
        # total size
        size = get_folder_size(dirpath)

        # write to the CSV file
        logFile.write(str(str(scanFile) + ',' + dirpath + ',' + str(size) + '\n'))

        logFileDir = str('D:\SYSTEM SCAN LOGS\\' + scanFile + '.csv')

    print(logFileDir)

    logFile.close()

    with open(logFileDir, 'r') as newData, open(oldData, 'r') as oldData:

        compare_data(newData, oldData)


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


def compare_data(newLog, oldLog):
    # this function compares the new scan Log to the old Log to determine if, and how much, memory space has changed
    # within each directory
    # both arguments should be filenames of the logs

    # use the .csv library to create dictionary objects out of files and read thru them
    newReader = csv.DictReader(newLog)
    oldReader = csv.DictReader(oldLog)

    oldDirs, newDirs = [], []

    # write data from new log into dictionary list
    for row in newReader:
        newLogData = {}

        newLogData['ScanDate'] = row['ScanDate']
        newLogData['Directory'] = row['Directory']
        newLogData['Size'] = int(row['Size'])

        newDirs.append(newLogData)

    # write data from old log into another dictionary list
    for row in oldReader:
        oldLogData = {}

        oldLogData['ScanDate'] = row['ScanDate']
        oldLogData['Directory'] = row['Directory']
        oldLogData['Size'] = int(row['Size'])

        oldDirs.append(oldLogData)

    # now compare data between the two dict lists to determine what's changed

    for newDir in newDirs:
        for oldDir in oldDirs:

            if newDir['Directory'] == oldDir['Directory']:
                # we have linked dirs. now check to see if their size has changed

                if newDir['Size'] != oldDir['Size']:

                    print(newDir['Directory'], 'has changed in size! It used to be', oldDir['Size'],
                          'bytes, now it\'s', newDir['Size'], 'bytes! Hype')

    # now that we have determined changes, now we should check for unique dirs
    # unique meaning either a dir that has been deleted since last scan, or a new dir added since last scan

    find_unique_dirs(oldDirs, newDirs)
    newLog.close()
    oldLog.close()


def find_old_log(dir):

    files = os.listdir(dir)
    paths = [os.path.join(dir, basename) for basename in files]
    newest_file = max(paths, key=os.path.getctime)

    return True, newest_file


def find_unique_dirs(oldDirs, newDirs):

    old_unmatched_dirs = []
    new_unmatched_dirs = []

    print('Old dirs:', str(len(oldDirs)))
    print('New dirs:', str(len(newDirs)))

    old_res = [sub['Directory'] for sub in oldDirs]
    new_res = [sub['Directory'] for sub in newDirs]

    for dircheck in old_res:
        if dircheck not in new_res:
            old_unmatched_dirs.append(dircheck)

    for dircheck in new_res:
        if dircheck not in old_res:
            new_unmatched_dirs.append(dircheck)

    print(str(old_res), '\n' + str(new_res))

    print('Deleted/moved directories:', str(old_unmatched_dirs))
    print('Added directories:', str(new_unmatched_dirs))


main()
