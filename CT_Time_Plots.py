from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import numpy as np
import pandas as pd
import tkinter as tk
from tkinterdnd2 import *

# Constants
LIGHT_BLUE = "#CCEDFF"

# Functions
def drop_in_text(event):
    entry_sv.set(event.data)
    entry_path.delete("1.0", "end")
    entry_path.insert("end", entry_sv.get())

def on_entry_click_path(self):
    if entry_path.get() == "Enter File Path":
        entry_path.delete(0, "end")
        entry_path.insert(0, '')

def on_entry_click_title(self):
    if entry_title.get() == "Enter Plot Title":
        entry_title.delete(0, "end")
        entry_title.insert(0, '')

def on_focusout_path(self):
    if entry_path.get() == '':
        entry_path.insert(0, "Enter File Path")

def on_focusout_title(self):
    if entry_title.get() == '':
        entry_title.insert(0, "Enter Plot Title")

# Create main window
window = tk.Tk()
window.geometry("600x200")
window.resizable(0,0)
window.title("CT Time Plotter")

# Create labels frame
frame_lab = tk.Frame(window, height=50, bg=LIGHT_BLUE)
frame_lab.pack(expand=True, fill="both")

# Create entries and button frame
frame_eb = tk.Frame(window)
frame_eb.pack(expand=True)

# Create Labels
label1 = tk.Label(frame_lab, text='Please enter your file path with .xlsx included and plot title.')
label1.config(font=("Calibri", 16), bg=LIGHT_BLUE)
label1.pack(pady=3)

label2 = tk.Label(frame_lab, text=r'Example: "C:\Users\Bob\Desktop\Data.xlsx"')
label2.config(font=("Calibri", 16), bg=LIGHT_BLUE)
label2.pack(pady=7)

# Create entry fields
entry_sv = tk.StringVar()
entry_path = tk.Entry(frame_eb, textvariable=entry_sv, width=60)
#entry_path.drop_target_register(DND_FILES)
#entry_path.dnd_bind("<<Drop>>", drop_in_text)
entry_path.insert(tk.END, "Enter File Path")
entry_path.bind('<FocusIn>', on_entry_click_path)
entry_path.bind('<FocusOut>', on_focusout_path)

entry_title = tk.Entry(frame_eb, width=30)
entry_title.insert(0, "Enter Plot Title")
entry_title.bind('<FocusIn>', on_entry_click_title)
entry_title.bind('<FocusOut>', on_focusout_title)

var1 = tk.IntVar()
check_box = tk.Checkbutton(frame_eb, text="Invert Y-axis?", variable=var1, onvalue=1, offvalue=0)

def make_graph(event):
    # styles
    from matplotlib import style
    plt.style.use("seaborn-deep")
    fig, ax = plt.subplots()

    # data
    # droppedFile = sys.argv[1]
    droppedFile = entry_path.get()
    data = pd.read_excel(droppedFile)
    temp = data.columns
    data.columns = data.columns.str.replace(' ', '')
    data.columns = data.columns.str.lower()
    date_x = np.array(data["wwdateofcollection"])
    ct_y = np.array(data["ct/n1(internal)"])
    ct_y[ct_y == 0] = np.nan
    mask = np.isfinite(ct_y)
    data.columns = temp

    # plot
    if var1.get() == 1:
        ax.set_ylim([42,0])
    else:
        ax.set_ylim([0, 42])
    ax.plot(date_x[mask], ct_y[mask], marker=".")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=(6, 12, 18, 24)))
    for label in ax.get_xticklabels(which="major"):
        label.set(rotation=45, horizontalalignment="right")
    ax.grid(axis="y", color="gray", alpha=0.5)

    plt.subplots_adjust(bottom=0.25)
    title = entry_title.get()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("CT Score")

    plt.tight_layout()

    plt.show(block=True)

button = tk.Button(frame_eb, text='Make Graph')
button.config(font=("Calibri", 12))
button.bind("<Button-1>", make_graph)
window.bind("<Return>", make_graph)

# Organize layout
entry_path.grid(row=0, padx=100)
entry_title.grid(row=1, padx=50)
check_box.grid(row=2, padx=50)
button.grid(row=3, padx=50)

# Run
window.mainloop()
