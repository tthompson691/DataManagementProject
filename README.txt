~~~SPOTLIGHT~~~

As a musician and music producer, I am constantly creating and working with a huge amount of uncompressed media files. This
means that I am constantly battling hard drive space issues as all these media files quickly fill up my drive. Upon looking through
my drive, it actually has proven to be quite challenging to locate where all these automatically-saved media files are stored. The
plethora of different softwares and project directories I utilize means that most of this media is stored quite deep down in
folder structures that are hard to identify. Because Windows explorer doesn't show a folder's size in the information column,
I would have to right-click folders to check their properties, and tediously engage in a blind search until I could uncover where
lots of this media resides.

So I decided to streamline this process with python! My app, called Spotlight, will quickly search through whatever directory
you give it, and return two main informational graphics:

1) a pie chart showing the size of all the subdirectories of the given search directory
2) A line chart showing the history of the size of the search directory over time

In addition to the graphs, Spotlight will also create buttons for each subdirectory of the currently viewed directory. If one of these
buttons is clicked, new graphics will generate for the new directory, as well as a new set of subdirectory buttons! A "back" button
is also generated so the user can return to the previous directory if they desire.

With this streamlined interface, it is now far easier to identify where all that bulky media is hiding in your hard drive! You might also discover
long-forgotten huge project folders that you can safely move to a different drive.


HOW IT WORKS:
Spotlight is powered by Python and utilizes the os, csv, matplotlib, and tkinter libraries.

Scan data is stored and referenced in csv files that are stored in a user-specified location. If this is the first scan of a
particular directory, a brand new csv file will be created with an appropriate name. If this is NOT the first scan of that directory,
data will be appended to the existing scan log of that directory.

The primary scan function uses two nested os.walk() commands to calculate and gather the size of each subdirectory (and their
subdirectories, and so on) and writes three data points to the scan log: directory name, scan date, and directory size. It has built in
try/except clauses to handle the occasional permission error when attempting to access a directory with os.walk.

The graphs are created with matplotlib and reference data in the scan logs. To avoid a messy pie chart in the even that a directory
has a ton of subdirectories, only subdirectories that are >10% of the largest subdirectory are displayed, while the remaining
subdirs are lumped into an "other" category with its own slice. In addition to subdirs, the actual files within a directory
(note: not the files within the subdirs) are lumped together for their own slice as well.

Finally, the GUI is powered by tkinter. Before the scan function is available to execute, the user must first supply 1) a directory
in which to store scan logs and 2) the directory to be scanned. Both of these selections are made with an easy folder selection
tool. After the scan is complete, navigation buttons are also generated so the user can "follow the trail" of bulky folders if they
want. One button is created for each of the qualifying subdirectories, as well as a "back" button, which will navigate the user
up one folder. This button is only available if the user has first navigated forwards.