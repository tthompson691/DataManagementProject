from tkinter import filedialog
from tkinter import *
from main import main
import graphs
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


root = Tk()

launch_frame = Frame(root)

t = Text(master=launch_frame, height=1, width=30)

# main scan button
mainButton = Button(master=launch_frame, text="SCAN!", state=DISABLED)

# select directory button
dirButton = Button(master=launch_frame, text="Select scan directory...", command=lambda: get_directory(t, mainButton))

def get_directory(text, mainButton):
    # first clear form if it already has text
    try:
        text.delete("1.0", END)
    except AttributeError:
        pass

    directory = filedialog.askdirectory().replace('/', '\\')
    print(directory)
    text.insert(END, directory)

    # on the off chance the user just cancels out the file explorer dialogue, keep scan button disabled
    if text.get("1.0", END) != '\n':
        mainButton['state'] = NORMAL
        mainButton['command'] = lambda: scan_and_display(directory)
    else:
        mainButton['state'] = DISABLED

    return directory


def scan_and_display(directory):
    # runs the main scan function
    data, scanDate = main(directory)
    display(directory, data, scanDate)


def display(directory, data, scan_date):
    graph_frame = Frame(root, height=1000, width=1200)

    dataset1 = Dataset(data, directory, scan_date, graph_frame)

    # create a pie chart, and store the subdirectories for easy button navigation
    sub_dirs = dataset1.pie_chart()
    dataset1.line_chart()
    graph_frame.grid(row=0, column=2)

    button_frame = Frame(root)

    r = 0
    for item in sub_dirs:
        Button(master=button_frame, text=item).grid(column=3, row=r)
        r += 1

    button_frame.grid(row=0, column=3)

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



# dirButton.pack()
# mainButton.pack()
# t.pack()

dirButton.grid(row=0, column=0)
mainButton.grid(row=1, column=0)
t.grid(row=0, column=1)
launch_frame.grid(row=0, column=0)

root.mainloop()
