"""
A heavily modified version of my intro to CS final.

It's a simple text editor, which will eventually feature 
syntax highlighting, proper editor panes, and hopefully more.
"""

# Import the tkinter and sys libraries.
from tkinter import filedialog
import tkinter as tk
import text as text # Import some custom UI elements
import config as config # Import the file to parse config files.
import sys  # For sys.exit

class Window(tk.Tk):
  def __init__(self, title, conf_path, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    self.win_title = title

    self.copy_buffer = None
    self.line_num = 0
    self.col_num  = 0
    
    self.current_file = ''
    self.supported_filetypes = [
      ("All Files", "*.*"),
      ("Text Files", "*.txt"),
      ("Python Files", "*.py")
    ]

    self.title(title)
    self.geometry('800x600')

    self.cfg = config.generate_config(conf_path)

    self.text_field = text.EditPannel(self)                           \
      .set_font(self.cfg['font']['family'], self.cfg['font']['size']) \
      .set_bg_col(self.cfg['colors']['bg'])                           \
      .set_txt_col(self.cfg['colors']['txt'])                         \
    
    self.text_entry_field = self.text_field.text

    self.text_field.pack(side='top', fill='both', expand=True)

    self.statusbar = text.Statusbar(self)
    self.status_line = text.StatusbarElem(self.statusbar)
    status_line_text = tk.Label(self.status_line, text='ln 1 : col 0')
    self.status_line.element(status_line_text)
    self.statusbar.add_element(self.status_line) \
                  .draw()                        \

    self.text_entry_field.change_tabstop(self.cfg['font']['tabstop']*2)
    self.text_entry_field.add_event_on_keypress(self.update_line_num)
    self.text_entry_field.add_event_on_mouse_event(self.update_line_num)

    # The menubar
    menubar = tk.Menu(self)
    file_menu = tk.Menu(menubar, tearoff=0)
    edit_menu = tk.Menu(menubar, tearoff=0)
    
    file_menu.add_command(label='Open', command=self.open_file)
    file_menu.add_command(label='Save', command=self.save_file)
    file_menu.add_command(label='Save As', command=self.save_file_as)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=sys.exit)
    
    edit_menu.add_command(label='Cut', command=self.cut_selection)
    edit_menu.add_command(label='Copy', command=self.copy_selection)
    edit_menu.add_command(label='Paste', command=self.paste)

    menubar.add_cascade(label='File', menu=file_menu)
    menubar.add_cascade(label='Edit', menu=edit_menu)

    self.bind('<Control-o>', self.open_file)
    self.bind('<Control-s>', self.save_file)
    self.bind('<Control-S>', self.save_file_as)

    self.bind('<Control-x>', self.cut_selection)
    self.bind('<Control-c>', self.copy_selection)
    self.bind('<Control-v>', self.paste)

    self.config(menu=menubar)

  def update_line_num(self, e):
    self.line_num, self.col_num = self.text_entry_field.index('insert').split('.')
    self.status_line.elem.configure(text=f'ln {self.line_num} : col {self.col_num}')
    self.statusbar.draw()

  def open_file(self, e=None):
    filepath = filedialog.askopenfilename(filetypes=self.supported_filetypes)

    if filepath == '':
      return

    self.current_file = filepath

    self.text_entry_field.delete('1.0', tk.END)

    with open(filepath, mode='r', encoding='utf-8') as input_file:
      file_text = input_file.read()
      self.text_entry_field.insert('1.0', file_text)

    self.title(f"{self.win_title} - {filepath}")

  def save_file_as(self, e=None):
    filepath = filedialog.asksaveasfilename(
      defaultextension='.txt',
      filetypes=self.supported_filetypes
    )

    if filepath == '':
      return

    self.current_file = filepath

    with open(filepath, mode='w', encoding='utf-8') as output_file:
      file_text = self.text_entry_field.get('1.0', tk.END)
      output_file.write(file_text)

    self.title(f'{self.win_title} - {filepath}')

  def save_file(self, e=None):
    if self.current_file == '':
      self.save_file_as(e)
      return

    with open(self.current_file, mode='w', encoding='utf-8') as output_file:
      file_text = self.text_entry_field.get('1.0', tk.END)
      output_file.write(file_text)

  def copy_selection(self, e=None):
    selection = self.text_entry_field.get(f'{self.line_num}.{self.col_num}')[1:]
    if selection:
      self.copy_buffer = selection

  def cut_selection(self, e=None):
    selection = self.text_entry_field.get(f'{self.line_num}.{self.col_num}')[1:]
    if selection:
      self.copy_buffer =selection
      self.text_entry_field.delete('sel.first', 'sel.last')

  def paste(self, e=None):
    if self.copy_buffer: 
      self.text_entry_field.insert(f'{self.line_num}.{self.col_num}', self.copy_buffer)


win = Window('PyEd', 'cfg/config.yaml')
win.mainloop()
