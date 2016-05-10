from tkinter import Tk, Text, StringVar
from tkinter.ttk import Style, Frame, Label, Button

class BoxFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, style='box.TFrame')
        self._position = (-1,-1)

        self.label_text = StringVar(self, '(,)')
        lbl = Label(self, textvariable=self.label_text)
        lbl.pack()

    def set_position(self, position, main_window):
        self._position = position
        self.label_text.set(str(self._position))
