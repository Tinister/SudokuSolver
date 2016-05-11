from tkinter import Tk, Text, StringVar
from tkinter.ttk import Style, Frame, Label, Button


def _build_grids(parent_frame, parent_position, types_list, mainframe):
    if len(types_list) <= 0:
        return
    parent_frame.rowconfigure((0, 1, 2), weight=1)
    parent_frame.columnconfigure((0, 1, 2), weight=1)

    for row in (0, 1, 2):
        for col in (0, 1, 2):
            position = (row, col)

            subframe = types_list[0](parent_frame)
            subframe.place_at_position(position, parent_position, mainframe)

            _build_grids(subframe, position, types_list[1:], mainframe)


class SubGridFrame(Frame):
    _padding = 3

    def __init__(self, master):
        Frame.__init__(self, master, style='subgrid.TFrame')
        self.position = (-1, -1)

    def place_at_position(self, position, parent_position, mainframe):
        row = position[0]
        col = position[1]
        self.position = position

        padx = (SubGridFrame._padding, 0) if col < 2 else SubGridFrame._padding
        pady = (SubGridFrame._padding, 0) if row < 2 else SubGridFrame._padding
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')


class BoxFrame(Frame):
    _padding = 1

    def __init__(self, master):
        Frame.__init__(self, master, style='box.TFrame')
        self.position = (-1, -1)
        self.number_text = StringVar(self, '0')

        self.contents = Frame(self, width=30, height=30, style='box.TFrame')
        self.contents.pencil_marks = [None] * 9
        self.number = Label(self.contents, textvariable=self.number_text, style='number.TLabel')

    def place_at_position(self, position, parent_position, mainframe):
        row = position[0]
        col = position[1]
        self.position = (parent_position[0] * 3 + row, parent_position[1] * 3 + col)
        self.number_text.set(str(row * 3 + col + 1))

        mainframe.boxes[self.position] = self
        _build_grids(self.contents, (0, 0), [PencilFrame], mainframe)

        padx = (0, BoxFrame._padding) if col < 2 else 0
        pady = (0, BoxFrame._padding) if row < 2 else 0
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')
        self.contents.pack(padx=2, pady=2, expand=True)
        self.number.place(relx=0.5, rely=0.5, anchor='center')

    def show_pencils(self):
        for widget in self.contents.pack_slaves():
            widget.pack_forget()
        for widget in self.contents.pencil_marks:
            widget.grid(row=widget.position[0], column=widget.position[1], sticky='nesw')


class PencilFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=10, height=10, style='box.TFrame')
        self.position = (-1, -1)

    def place_at_position(self, position, parent_position, mainframe):
        row = position[0]
        col = position[1]
        self.position = position
        frame_index = row * 3 + col

        self.master.pencil_marks[frame_index] = self
        #self.grid(row=row, column=col, sticky='nesw')

        number = Label(self, text=str(frame_index + 1), style='pencil.TLabel')
        number.place(relx=0.5, rely=0.5, anchor='center')


class BorderFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, style='red.TFrame')
        self.place(relwidth=1.0, height=2, x=0, y=0, anchor='nw')
