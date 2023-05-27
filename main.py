"""
Python - Final Project

A simple text editor.

Features:
    - Line numbers
    - Saving & Opening files
    - Simple UI
    - Simple configuration
    - Syntax highlighting
"""

# Import the tkinter and sys libraries.
from idlelib.colorizer import ColorDelegator # IDLE syntax highlighting
from idlelib.percolator import Percolator
from tkinter import filedialog
import tkinter as tk
import text # Import some custom UI elements
import config # Import the file to parse config files.
import sys  # For sys.exit

title = "Notepad 2.1/2"

cfg = config.generate_config("cfg/config.yaml")

# Create a window
win = tk.Tk()
win.title(title)
win.geometry("800x600")

cdg = ColorDelegator() # Colors!
cdg.tagdefs['COMMENT'] = {
    'foreground': cfg["colors"]["highlighting"]["comment"],
    'background': cfg["colors"]["bg"]
}
cdg.tagdefs['KEYWORD'] = {
    'foreground': cfg["colors"]["highlighting"]["kwd"],
    'background': cfg["colors"]["bg"]
}
cdg.tagdefs['BUILTIN'] = {
    'foreground': cfg["colors"]["highlighting"]["builtin"],
    'background': cfg["colors"]["bg"]
}
cdg.tagdefs['STRING'] = {
    'foreground': cfg["colors"]["highlighting"]["string"],
    'background': cfg["colors"]["bg"]
}
cdg.tagdefs['DEFINITION'] = {
    'foreground': cfg["colors"]["highlighting"]["definition"],
    'background': cfg["colors"]["bg"]
}

# The text entry box
txt_field = text.EditPannel(win)
txt_entry = txt_field.text
txt_field.set_font(cfg["font"]["family"], cfg["font"]["size"])
txt_field.set_bg_col(cfg["colors"]["bg"])
txt_field.set_txt_col(cfg["colors"]["txt"])
txt_field.pack(side="top", fill="both", expand=True)
Percolator(txt_entry).insertfilter(cdg)

txt_entry.change_tabstop(cfg["font"]["tabstop"]*2)

# Statusbar
statusbar = text.Statusbar(win)

status_line = text.StatusbarElem(statusbar)
status_line_txt = tk.Label(status_line, text="ln 1 : col 0")
status_line.set_elem(status_line_txt)

statusbar.add_elem(status_line)

def update_line_num(event):
    line_num, col_num = txt_entry.index("insert").split('.')
    status_line_txt.configure(text=f"ln {line_num} : col {col_num}")

    statusbar.draw()

txt_entry.add_event_on_keypress(update_line_num)
txt_entry.add_event_on_mouse_event(update_line_num)

statusbar.draw()

current_file = ""

supported_filetypes = [
    ("All Files", "*.*"),
    ("Text Files", "*.txt"),
    ("Python Files", "*.py")
]

# The file dialogs to open and save files. 
def open_file():
    """Open a file for editing."""
    global current_file
    filepath = filedialog.askopenfilename(
        filetypes=supported_filetypes
    )

    if filepath == "":
        return

    current_file = filepath

    txt_field.text.delete("1.0", tk.END)

    with open(filepath, mode="r", encoding="utf-8") as input_file:
        file_text = input_file.read()
        txt_field.text.insert(tk.END, file_text)

    win.title(f"{title} - {filepath}")

def save_file_as():
    """Save the current file as a new file."""
    global current_file
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=supported_filetypes
    )

    if filepath == "":
        return

    current_file = filepath

    with open(filepath, mode="w", encoding="utf-8") as output_file:
        file_text = txt_field.text.get("1.0", tk.END)
        output_file.write(file_text)

    win.title(f"{title} - {filepath}")

def save_file():
    """Save the current file"""
    if current_file == "":
        save_file_as()
        return

    with open(current_file, mode="w", encoding="utf-8") as output_file:
        file_text = txt_field.text.get("1.0", tk.END)
        output_file.write(file_text)

# The menubar
menubar = tk.Menu(win)
file_menu = tk.Menu(menubar, tearoff=0)

# file_menu.add_command(label="New")
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=sys.exit)
menubar.add_cascade(label="File", menu=file_menu)

def open_cmd(e):
    open_file()


def save_cmd(e):
    save_file()

def quit_cmd(e):
    sys.exit(0)

# Configure the window, and run the main loop. 
win.config(menu=menubar)

win.bind('<Control-o>', open_cmd) # Open file shortcut
win.bind('<Control-s>', save_cmd) # Save file shortcut
win.bind('<Control-q>', quit_cmd) # Quit command shortcut
win.mainloop()

