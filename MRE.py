from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Progressbar
from main import main
import graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
import threading

root = Tk()

launch_frame = Frame(root)
button_frame = Frame(root)
graph_frame = Frame(root, height=1000, width=1200)


# log directory button/text
logDirButton = Button(master=launch_frame, text='Select log storage location...',
                      command=lambda: get_directory(log_text), width=22)
log_text = Text(master=launch_frame, height=1, width=25)
logDirButton.grid(row=1, column=0)
log_text.grid(row=1, column=1)

# scan directory button/text
dirButton = Button(master=launch_frame, text="Select scan directory...", command=lambda: get_directory(t), width=22)
t = Text(master=launch_frame, height=1, width=25)
dirButton.grid(row=2, column=0)
t.grid(row=2, column=1)

# main scan button
# style = Style()
# style.configure('ScanButton', font=('Chambers', 20), borderwidth='4')
mainButton = Button(master=launch_frame, text="SCAN!", state=DISABLED,
                    width=50, height=10, bg='#27b355')
mainButton.grid(row=3, column=0, columnspan=2)

# progress bar
progress = Progressbar(launch_frame, orient=HORIZONTAL, length=100, mode='indeterminate')
progress.grid(row=4, column=0, columnspan=2)

launch_frame.grid(row=0, column=0, sticky=NW)

nav_history = []

def get_directory(text):
    # first clear form if it already has text
    try:
        text.delete("1.0", END)
    except AttributeError:
        pass

    directory = filedialog.askdirectory()
    # store the first directory for later specific reference

    text.insert(END, directory)

    # disable scan button until user has given necessary info to run (log storage location, scan directory)
    enable_scan_button(log_text, t)

    return directory


def enable_scan_button(logText, dirText):
    if logText.get("1.0", END) != '\n' and dirText.get('1.0', END) != '\n':
        mainButton['state'] = NORMAL
        mainButton['command'] = lambda: scan_and_display()
    else:
        mainButton['state'] = DISABLED


def scan_and_display():

    threading.Thread(target=bar_start).start()
    # get scan directory and log directory from text fields
    log_directory = log_text.get("1.0", END)[:-1]
    scan_directory = t.get("1.0", END)[:-1]

    # store the initial scan directory for later reference
    top_dir = scan_directory

    # runs the main scan function. Passes scan_directory and log_directory arguments
    data, scanDate = main(log_directory, scan_directory)
    display(scan_directory, data, scanDate, top_dir)
    # bar_stop()


def display(directory, data, scan_date, top_dir):
    # first clear the graphs area of any existing graphs
    graph_frame.grid(row=0, column=2, sticky="ensw")
    for graph in graph_frame.winfo_children():
        graph.destroy()

    print("early: ", directory)
    print("data: ", data)
    print("scan_date: ", scan_date)

    # add current directory to nav_history, for later reference to back_button
    nav_history.append(directory)

    dataset1 = Dataset(data, directory, scan_date, graph_frame)

    # create a pie chart, and store the subdirectories for easy button navigation
    sub_dirs = dataset1.pie_chart()
    print("Sub dirs for buttons: ", sub_dirs)
    # also create line chart to display the drive's history
    dataset1.line_chart()

    # if nav buttons already exist, clear them out to make room for new set of buttons
    for button in button_frame.winfo_children():
        button.destroy()

    # create buttons to easily jump to a subdirectory breakdown
    r = 0
    for item in sub_dirs[:-2]:
        # extract names of subdirectories and create full directory names to pass to buttons
        # skip the "files" and "other" labels (will always be the last two)
        dirname = item.split(":")[0]

        if directory[-1] == '/':
            fulldir = directory + dirname
        else:
            fulldir = directory + '/' + dirname

        # print("button creation:", fulldir)
        b = Nav_button(button_frame, item, fulldir, data, scan_date, top_dir).create()
        b.grid(column=3, row=r, sticky=E)

        r += 1

    # create back button. Ensure it's only available if it makes sense
    if top_dir != directory:
        back_dir_list = directory.split('/')[:-1]
        separator = '/'
        back_dir = separator.join(back_dir_list)
        print("BACK_DIR:", back_dir)

        # account for letter drive naming quirk
        if back_dir[-1] == ':':
            back_dir += '/'

        # print("backdir:", back_dir)

        back = Nav_button(button_frame, "Back", back_dir, data, scan_date, top_dir).create()
        back.grid(column=3, row=r, sticky=E)
        progress.destroy()

    button_frame.grid(row=0, column=3, sticky=E)


def bar_start():
    print("BAR START CALLED")
    progress.start(10)


def bar_stop():
    progress.stop()

class Dataset:
    def __init__(self, data, directory, scan_date, frame):
        self.data = data
        self.directory = directory
        self.scan_date = scan_date
        self.frame = frame

    def pie_chart(self):
        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass

        print("SELF DATA:", self.data)
        print("SELF DIRECTORY:", self.directory)
        print("SELF SCAN:", self.scan_date)

        self.piechart, self.labels = graphs.make_pie_chart(self.data, self.directory, self.scan_date)
        self.canvas = FigureCanvasTkAgg(self.piechart, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        return self.labels

    def line_chart(self):
        linechart = graphs.make_line_chart(self.data, self.directory)
        self.canvas2 = FigureCanvasTkAgg(linechart, master=self.frame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack()


class Nav_button:
    def __init__(self, frame, text, fulldir, data, scan_date, top_dir):
        self.frame = frame
        self.text = text
        self.fulldir = fulldir
        self.data = data
        self.scan_date = scan_date
        self.top_dir = top_dir

    def create(self):
        return Button(master=self.frame, text=self.text,
                      command=lambda: display(self.fulldir, self.data, self.scan_date, self.top_dir))


root.mainloop()
