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
import text as text # Import some custom UI elements
import config as config # Import the file to parse config files.
import sys  # For sys.exit

copy_buffer = []
current_ln = 0
current_col = 0

title = "Notepad 2.1/2"

cfg = config.generate_config("cfg/config.yaml")

# Create a window
win = tk.Tk()
win.title(title)
win.geometry("720x1280")

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

def update_line_num(e):
  global current_col, current_ln
  current_ln, current_col = txt_entry.index("insert").split('.')
  status_line_txt.configure(text=f"ln {current_ln} : col {current_col}")

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
def open_file(e=None):
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

def save_file_as(e=None):
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

def save_file(e=None):
  """Save the current file"""
  if current_file == "":
    save_file_as()
    return

  with open(current_file, mode="w", encoding="utf-8") as output_file:
    file_text = txt_field.text.get("1.0", tk.END)
    output_file.write(file_text)

def copy_cmd(e=None):
  if txt_entry.selection_get():
    copy_buffer.append(txt_entry.selection_get())

def paste_cmd(e=None):
  if copy_buffer.len() > 0: 
    txt_entry.insert(f"{current_ln}.{current_col}", copy_buffer[len(copy_buffer)-1])

def cut_cmd(e=None):
  if txt_entry.selection_get():
    copy_buffer.append(txt_entry.selection_get())
    txt_entry.delete('sel.first', 'sel.last')

# The menubar
menubar = tk.Menu(win)
file_menu = tk.Menu(menubar, tearoff=0)

# file_menu.add_command(label="New")
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_file_as)
file_menu.add_command(label="Cut", command=cut_cmd)
file_menu.add_command(label="Copy", command=copy_cmd)
file_menu.add_command(label="Paste", command=paste_cmd)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=sys.exit)
menubar.add_cascade(label="File", menu=file_menu)

win.bind('<Control-o>', open_file)
win.bind('<Control-s>', save_file)
win.bind('<Control-S>', save_file_as)

win.bind('<Control-x>', cut_cmd)
win.bind('<Control-c>', copy_cmd)
win.bind('<Control-v>', paste_cmd)

# Configure the window, and run the main loop. 
win.config(menu=menubar)
win.mainloop()



