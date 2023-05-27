import tkinter.font as tkfont
from tkinter import ttk
import tkinter as tk

class CText(tk.Text):
  def __init__(self, *args, **kwargs):
    tk.Text.__init__(self, *args, **kwargs)

    self.tabsize = 4
    font = tkfont.Font()
    tab = font.measure(' ' * self.tabsize)
    self.config(tabs=tab)
    
    # create a proxy for the underlying widget
    self._orig = "_orig"
    self.tk.call("rename", self._w, self._orig)
    self.tk.createcommand(self._w, self._proxy)

  def add_event_on_keypress(self, func):
    self.bind("<KeyRelease>", func)

  def add_event_on_mouse_event(self, func):
    self.bind("<ButtonRelease>", func)

  def change_tabstop(self, tabstop):
    self.tabsize = tabstop
    font = tkfont.Font()
    tab = font.measure(' ' * self.tabsize)
    self.config(tabs=tab)

  def _proxy(self, *args):
    # let the actual widget perform the requested action
    cmd = (self._orig,) + args
    try:
      result = self.tk.call(cmd)
      # generate an event if something was added or deleted,
      # or the cursor position changed
      if (args[0] in ("insert", "replace", "delete") or 
        args[0:3] == ("mark", "set", "insert") or
        args[0:2] == ("xview", "moveto") or
        args[0:2] == ("xview", "scroll") or
        args[0:2] == ("yview", "moveto") or
        args[0:2] == ("yview", "scroll")
      ):
        self.event_generate("<<Change>>", when="tail")
      # return what the actual widget returned
      return result
    except Exception:
      pass # Ignore the error thrown when you paste stuff. 

class TextLineNumbers(tk.Canvas):
  color = "#000000" # A Default color for text.

  def __init__(self, *args, **kwargs):
    tk.Canvas.__init__(self, *args, **kwargs)
    self.textwidget = None
    self.font = "Arial", 12

  def attach(self, text_widget):
    self.textwidget = text_widget
  
  def set_font(self, fnt):
    self.font = fnt

  def set_col(self, color):
    self.color = color
      
  def redraw(self, *args):
    """redraw line numbers"""
    self.delete("all")
    i = self.textwidget.index("@0,0")
    while True :
      dline= self.textwidget.dlineinfo(i)
      if dline is None: break
      y = dline[1]
      linenum = str(i).split(".")[0]
      self.create_text(2,y,anchor="nw", text=linenum, fill=self.color, font=self.font)
      i = self.textwidget.index("%s+1line" % i)

class Statusbar(tk.Frame):
  def __init__(self, root):
    super().__init__(root, borderwidth=1, relief="raised")
    self.elems = []

  def add_element(self, elem):
    self.elems.append(elem)
    return self

  def draw(self):
    for i in range(len(self.elems)):
      self.elems[i].draw()
      if i != len(self.elems)-1:
        sp = ttk.Separator(self, orient="vertical")
        sp.pack(fill="y", side="right")
    self.pack(side="bottom", fill="x")

class StatusbarElem(tk.Frame):
  def __init__(self, root, element=None, *, side='right', fill='x', padx=10, pady=0):
    super().__init__(root)
    self.elem = element

    self.side = side
    self.fill = fill
    self.padx = padx
    self.pady = pady

  def element(self, elem):
    self.elem = elem
    return self

  def draw(self):
    self.elem.pack(anchor="e")
    self.pack(side=self.side, fill=self.fill, padx=self.padx, pady=self.pady)

class EditPannel(tk.Frame):
  def __init__(self, root):
    tk.Frame.__init__(self, root)
    self.text = CText(self)
    self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
    self.text.configure(yscrollcommand=self.vsb.set)
    self.text.configure(font=("Terminal", "10"))
    self.linenumbers = TextLineNumbers(self, width=60)
    self.linenumbers.attach(self.text)
    self.linenumbers.configure(bg="white")
    self.linenumbers.config(highlightbackground="white")
    self.text.config(highlightbackground="white")

    self.vsb.pack(side="right", fill="y")
    self.linenumbers.pack(side="left", fill="y")
    self.text.pack(side="right", fill="both", expand=True)

    self.text.bind("<<Change>>", self._on_change)
    self.text.bind("<Configure>", self._on_change)

  def set_font(self, fnt, size):
    self.text.configure(font=(fnt, size))
    self.linenumbers.set_font((fnt, size))
    return self
    
  def set_bg_col(self, color):
    self.text.configure(bg=color)
    self.linenumbers.configure(bg=color)
    self.text.config(highlightbackground="white")
    self.linenumbers.config(highlightbackground=color)
    return self

  def set_txt_col(self, color):
    self.text.configure(fg=color)   
    self.linenumbers.set_col(color)
    self.text.configure(insertbackground=color)
    return self

  def _on_change(self, e):
    self.linenumbers.redraw()
