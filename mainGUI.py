from tkinter import filedialog
from tkinter import *
from main import main
import graphs
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


root = Tk()

t = Text(root, height=2, width=30)

# main scan button
mainButton = Button(text="SCAN!", state=DISABLED)

# select directory button
dirButton = Button(text="Select scan directory...", command=lambda: get_directory(t, mainButton))


def get_directory(text, mainButton):
    text.delete("1.0", END)
    directory = filedialog.askdirectory().replace('/', '\\')
    text.insert(END, directory)

    # on the off chance the user just cancels out the file explorer dialogue, keep scan button disabled
    if text.get("1.0", END) != '\n':
        mainButton['state'] = NORMAL
        mainButton['command'] = lambda: scan_and_display(directory)
    else:
        mainButton['state'] = DISABLED

    return directory


def set_state(text, button):
    res = text.get("1.0", END)
    print("res: ", str(res))


def scan_and_display(directory):
    # runs the main scan function
    data, scanDate = main(directory)

    #instantiate frame for graph display
    gframe = Frame(root)
    try:
        gframe.get_tk_widget().pack_forget()
    except AttributeError:
        pass
    pieChart = graphs.make_pie_chart(data, directory, scanDate)

    canvas = FigureCanvasTkAgg(pieChart, master=gframe)
    canvas.draw()
    canvas.get_tk_widget().pack()

dirButton.pack()
mainButton.pack()
t.pack()

root.mainloop()
