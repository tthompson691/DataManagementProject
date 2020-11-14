
from matplotlib import pyplot as plt
import csv, os

plt.style.use("fivethirtyeight")


def make_pie_chart(data, top_dir, scanDate):

    labels = []
    values = []

    # extract string of top folder for later reference
    # example: if top_dir is D:\Music\Projects, extract "Projects"
    top_folder = top_dir.split("\\")[-1]
    print(top_folder)

    # first, parse data to prepare it for plotting
    with open(data, 'r') as data:
        reader = csv.DictReader(data)

        for row in reader:
            if row["Directory"].split("\\")[-2] == top_folder:
                labels.append(row["Directory"])
                values.append(int(row[scanDate]))

    print("Original values length:", str(len(values)))

    # remove values less than 10% of max and lump them into one "other" category
    displayed_vals = []
    displayed_labels = []
    others = []
    others_labels = []
    others_sum = 0
    i = 0

    max_size = max(values)
    print(max_size)

    for value in values:
        if value < max_size / 10:
            others.append(value)
            others_labels.append(labels[i].split("\\")[-1])
            others_sum += value
        else:
            displayed_vals.append(value)
            displayed_labels.append(labels[i].split("\\")[-1] + ": " + str(value) + " bytes")

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

    displayed_labels.append("Files")
    displayed_vals.append(f_size)

    print(labels)
    print(values)

    print(f)
    print(f_size)

    print(others_sum)

    print("New values length:", str(len(values)))
    print(len(others))

    fig1, ax1 = plt.subplots()
    ax1.pie(displayed_vals, labels=displayed_labels)
    plt.show()


# make_pie_chart(r"D:\SYSTEM SCAN LOGS\MASTER SYSTEM SCAN LOG.csv", "D:\Music\Proyectos\Instajams",
#                'Nov-14-2020 __ 15h 16m 31s')


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


make_line_chart(r"D:\SYSTEM SCAN LOGS\MASTER SYSTEM SCAN LOG.csv", "D:\Music\Proyectos\Instajams")



