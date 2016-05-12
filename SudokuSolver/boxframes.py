from enum import Enum
from tkinter import Tk, Text, StringVar
from tkinter.ttk import Style, Frame, Label, Button


class Styles(object):
    grid_frame = 'grid.TFrame'
    box_frame = 'box.TFrame'
    given_frame = 'given.TFrame'
    number_label = 'number.TLabel'
    given_label = 'given.TLabel'
    pencil_label = 'pencil.TLabel'
    green = 'green.TFrame'
    red = 'red.TFrame'

    @staticmethod
    def setup():
        s = Style()
        s.theme_use('default')
        s.configure(Styles.grid_frame, background='#888')
        s.configure(Styles.box_frame, background='white')
        s.configure(Styles.given_frame, background='#ddd')
        s.configure(Styles.number_label, background='white', font='Helvetica 24')
        s.configure(Styles.given_label, background='#ddd', font='Helvetica 24 bold')
        s.configure(Styles.pencil_label, background='white', font='Helvetica 8')
        s.configure(Styles.green, background='green')
        s.configure(Styles.red, background='red')


def _build_grids(parent_frame, parent_position, types_list):
    if len(types_list) <= 0:
        return
    parent_frame.rowconfigure((0, 1, 2), weight=1)
    parent_frame.columnconfigure((0, 1, 2), weight=1)

    for row in (0, 1, 2):
        for col in (0, 1, 2):
            position = (row, col)

            subframe = types_list[0](parent_frame)
            subframe.place_at_position(position, parent_position)

            _build_grids(subframe, position, types_list[1:])


class SubGridFrame(Frame):
    _padding = 4

    def __init__(self, master):
        Frame.__init__(self, master, style=Styles.grid_frame)
        self.position = (-1, -1)

    def place_at_position(self, position, parent_position):
        row = position[0]
        col = position[1]
        self.position = position

        padx = (SubGridFrame._padding, 0) if col < 2 else SubGridFrame._padding
        pady = (SubGridFrame._padding, 0) if row < 2 else SubGridFrame._padding
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')


class BoxFrame(Frame):
    _padding = 1
    all = dict()

    def __init__(self, master):
        Frame.__init__(self, master, style=Styles.box_frame)
        self.position = (-1, -1)
        self.number_text = StringVar(self, '0')

        self.borders = dict()
        for e in 'nesw':
            self.borders[e] = BorderFrame(self, e)

        self.content_frame = Frame(self, width=30, height=30, style=Styles.box_frame)
        self.content_frame.pencil_marks = [None] * 9
        self.number = Label(self.content_frame, textvariable=self.number_text, style=Styles.number_label)

    def place_at_position(self, position, parent_position):
        row = position[0]
        col = position[1]
        self.position = (parent_position[0] * 3 + row, parent_position[1] * 3 + col)
        self.number_text.set(str(row * 3 + col + 1))

        BoxFrame.all[self.position] = self
        _build_grids(self.content_frame, (0, 0), [PencilFrame])

        padx = (0, BoxFrame._padding) if col < 2 else 0
        pady = (0, BoxFrame._padding) if row < 2 else 0
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')
        
        self.content_frame.pack(padx=BorderFrame._width, pady=BorderFrame._width, expand=True)
        self.set_pencils(False)

    def set_pencils(self, flag):
        if flag:
            self.number.place_forget()
            for pencil_mark in self.content_frame.pencil_marks:
                pencil_mark.grid(row=pencil_mark.position[0], column=pencil_mark.position[1], sticky='nesw')
        else:
            for pencil_mark in self.content_frame.pencil_marks:
                pencil_mark.grid_forget()
            self.number.place(relx=0.5, rely=0.5, anchor='center')

    def set_given(self, flag):
        self['style'] = Styles.given_frame if flag else Styles.box_frame
        self.content_frame['style'] = Styles.given_frame if flag else Styles.box_frame
        self.number['style'] = Styles.given_label if flag else Styles.number_label

    def set_borders(self, color, edges='nesw'):
        for e in self.borders.keys():
            if e in edges:
                self.borders[e].set_color(color)
            else:
                self.borders[e].set_color(None)


class PencilFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=10, height=10, style=Styles.box_frame)
        self.position = (-1, -1)

    def place_at_position(self, position, parent_position):
        row = position[0]
        col = position[1]
        self.position = position
        frame_index = row * 3 + col

        self.master.pencil_marks[frame_index] = self

        number = Label(self, text=str(frame_index + 1), style=Styles.pencil_label)
        number.place(relx=0.5, rely=0.5, anchor='center')


class BorderFrame(Frame):
    _width = 4

    def __init__(self, master, edge):
        Frame.__init__(self, master)
        self.edge = edge

    def set_color(self, color):
        if color is None:
            self.place_forget()
            return

        self['style'] = getattr(Styles, color)
        if self.edge == 'n':
            self.place(relwidth=1.0, height=BorderFrame._width, x=0, y=0, anchor='nw')
        elif self.edge == 's':
            self.place(relwidth=1.0, height=BorderFrame._width, x=0, rely=1.0, anchor='sw')
        elif self.edge == 'w':
            self.place(width=BorderFrame._width, relheight=1.0, x=0, y=0, anchor='nw')
        else: # self.edge == 'e'
            self.place(width=BorderFrame._width, relheight=1.0, relx=1.0, y=0, anchor='ne')
