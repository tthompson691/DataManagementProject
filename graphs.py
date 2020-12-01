
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import csv, os


plt.style.use("fivethirtyeight")


def make_pie_chart(data, top_dir, scanDate):

    labels = []
    values = []

    # first, parse data to prepare it for plotting
    with open(data, 'r') as data:
        reader = csv.DictReader(data)

        for row in reader:
            if os.path.dirname(row["Directory"]) == top_dir and row["Directory"] != top_dir:
                labels.append(row["Directory"])
                values.append(int(row[scanDate]))

    # remove values less than 10% of max and lump them into one "other" category
    displayed_vals = []
    displayed_labels = []
    others = []
    others_labels = []
    others_sum = 0
    i = 0

    # if [values] is empty, that means the current directory only has files in it
    try:
        max_size = max(values)
    except ValueError:
        pass

    # to avoid overly messy chart, only display folders that are >10% of the largest folder's size. All other folders
    # will be lumped into the "others" category
    for value in values:
        if value < max_size / 10:
            others.append(value)
            others_labels.append(labels[i].split("/")[-1])
            others_sum += value
        else:
            displayed_vals.append(value)
            # convert size values to more legible GB,MB,KB etc values
            label_value = format_bytes(value)
            displayed_labels.append(labels[i].split("/")[-1] + ": " + str(label_value))

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
    print(displayed_labels)
    print(displayed_vals)
    fig = Figure()
    fig.suptitle(("Breakdown: " + str(top_dir)))
    p = fig.add_subplot(111)

    p.pie(displayed_vals, labels=displayed_labels)
    #plt.title("Breakdown: " + top_folder)
    #p.show()

    return fig, displayed_labels


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

    fig = Figure()

    p = fig.add_subplot(111)

    p.plot(display_labels, display_vals)

    # p.title("History: " + top_folder)
    # p.xlabel('Size (bytes)')
    # p.ylabel('Scan Date')
    # plt.show()

    return fig


def format_bytes(size):
    step_unit = 1024
    if type(size) == int:
        for i in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < step_unit:
                return "%3.1f %s" % (size, i)
            size /= step_unit
    else:
        return size


# make_pie_chart('D:\SYSTEM SCAN LOGS\MASTER SYSTEM SCAN LOG - D.csv', 'D:\\', 'Nov-18-2020 __ 12h 52m 06s')

#make_line_chart('D:\SYSTEM SCAN LOGS\MASTER SYSTEM SCAN LOG - .csv', 'C:\\')

