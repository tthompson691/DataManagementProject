
from matplotlib import pyplot as plt
import csv, os

plt.style.use("fivethirtyeight")


def make_pie_chart(data, top_dir, scanDate):

    labels = []
    values = []

    # extract string of top folder for later reference
    # example: if top_dir is D:\Music\Projects, extract "Projects"

    # if top_dir is a lettered drive, its naming convention will end in a slash. But if any other folder is chosen,
    # this isn't true. Since the log is parsed using slashes as split anchors, must account for this

    if top_dir.split('\\')[-1] == '':
        # true if passed a letter drive as top_dir
        top_folder = top_dir.split('\\')[-2]
    else:
        # true if passed any directory lower than a top letter drive
        top_folder = top_dir.split('\\')[-1]

    print(top_folder)
    # first, parse data to prepare it for plotting
    with open(data, 'r') as data:
        reader = csv.DictReader(data)

        for row in reader:
            if row["Directory"].split("\\")[-2] == top_folder and row["Directory"] != (top_folder + '\\'):
                labels.append(row["Directory"])
                print(row["Directory"])
                values.append(int(row[scanDate]))

    # remove values less than 10% of max and lump them into one "other" category
    displayed_vals = []
    displayed_labels = []
    others = []
    others_labels = []
    others_sum = 0
    i = 0

    max_size = max(values)

    for value in values:
        if value < max_size / 10:
            others.append(value)
            others_labels.append(labels[i].split("\\")[-1])
            others_sum += value
        else:
            displayed_vals.append(value)
            # convert size values to more legible GB,MB,KB etc values
            label_value = format_bytes(value)
            displayed_labels.append(labels[i].split("\\")[-1] + ": " + str(label_value))

        i += 1

    displayed_labels.append("Other(" + str(len(others)) + " folders)")
    displayed_vals.append(others_sum)

    # now add on the net size of all files in the top-level dir as the last datapoint
    f = []
    f_size = 0

    for (dirpath, dirnames, filenames) in os.walk(top_dir):
        os.chdir(top_dir)
        f.extend(filenames)
        for file in filenames:
            f_size += os.stat(file).st_size
        break

    displayed_labels.append("Files: " + str(format_bytes(f_size)))
    displayed_vals.append(f_size)

    plt.pie(displayed_vals, labels=displayed_labels)
    plt.title("Breakdown: " + top_folder)
    plt.show()


def make_line_chart(data, top_dir):

    display_vals = []
    display_labels = []

    with open(data, 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            if row["Directory"] == top_dir:
                print(row["Directory"])
                for item in row:
                    display_vals.append(row[item])
                    display_labels.append(item)

    plt.plot(display_labels, display_vals)
    plt.title("History: " + top_dir)
    plt.xlabel('Size (bytes)')
    plt.ylabel('Scan Date')
    plt.show()


def format_bytes(size):
    step_unit = 1024
    if type(size) == int:
        for i in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < step_unit:
                return "%3.1f %s" % (size, i)
            size /= step_unit
    else:
        return size


#make_pie_chart('D:\SYSTEM SCAN LOGS\MASTER SYSTEM SCAN LOG - .csv', 'C:\\Users\\tthom', 'Nov-17-2020 __ 11h 32m 41s')

make_line_chart('D:\SYSTEM SCAN LOGS\MASTER SYSTEM SCAN LOG - .csv', 'C:\\')

