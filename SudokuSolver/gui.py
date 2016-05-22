from tkinter import Tk, Text, StringVar
from tkinter.ttk import Style, Frame, Label, Button


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


def _tag_widget(widget, tag):
    widget.bindtags((tag,) + widget.bindtags())


def _find_parent(self, className):
    curr = self
    while True:
        if curr is None or type(curr) is className:
            return curr
        curr = curr.master
Frame.find_parent = _find_parent


class FrameStyles(object):
    grid_frame = 'grid.TFrame'
    box_frame = 'box.TFrame'
    given_frame = 'given.TFrame'
    number_label = 'number.TLabel'
    given_label = 'given.TLabel'
    pencil_label = 'pencil.TLabel'
    green = 'green.TFrame'
    red = 'red.TFrame'
    yellow = 'yellow.TFrame'

    @staticmethod
    def setup():
        s = Style()
        s.theme_use('default')
        s.configure(FrameStyles.grid_frame, background='#888')
        s.configure(FrameStyles.box_frame, background='white')
        s.configure(FrameStyles.given_frame, background='#ddd')
        s.configure(FrameStyles.number_label, background='white', font='Helvetica 24')
        s.configure(FrameStyles.given_label, background='#ddd', font='Helvetica 24 bold')
        s.configure(FrameStyles.pencil_label, background='white', font='Helvetica 8')
        s.configure(FrameStyles.green, background='green')
        s.configure(FrameStyles.red, background='red')
        s.configure(FrameStyles.yellow, background='yellow')


class SubGridFrame(Frame):
    _padding = 4

    def __init__(self, master):
        Frame.__init__(self, master, style=FrameStyles.grid_frame)
        self.position = (-1, -1)

    def place_at_position(self, position, parent_position):
        row = position[0]
        col = position[1]
        self.position = position
        self.find_parent(MainFrame).subgrids[self.position] = self

        padx = (SubGridFrame._padding, 0) if col < 2 else SubGridFrame._padding
        pady = (SubGridFrame._padding, 0) if row < 2 else SubGridFrame._padding
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')


class BoxFrame(Frame):
    _counter = 0;
    _padding = 1

    def __init__(self, master):
        Frame.__init__(self, master, style=FrameStyles.box_frame)
        self.position = (-1, -1)
        self.binding_tag = 'BoxFrame' + str(BoxFrame._counter)
        self.number_text = StringVar(self, '')
        BoxFrame._counter += 1

        self.borders = dict()
        for e in 'nesw':
            self.borders[e] = BorderFrame(self, e)

        self.content_frame = Frame(self, width=30, height=30, style=FrameStyles.box_frame)
        self.content_frame.pencil_marks = [None] * 9
        self.number = Label(self.content_frame, textvariable=self.number_text, style=FrameStyles.number_label)

    def place_at_position(self, position, parent_position):
        row = position[0]
        col = position[1]
        self.position = (parent_position[0] * 3 + row, parent_position[1] * 3 + col)

        _tag_widget(self, self.binding_tag)
        _tag_widget(self.content_frame, self.binding_tag)
        _tag_widget(self.number, self.binding_tag)

        self.find_parent(MainFrame).boxes[self.position] = self
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
        self['style'] = FrameStyles.given_frame if flag else FrameStyles.box_frame
        self.content_frame['style'] = FrameStyles.given_frame if flag else FrameStyles.box_frame
        self.number['style'] = FrameStyles.given_label if flag else FrameStyles.number_label

    def set_borders(self, color, edges='nesw'):
        for e in self.borders.keys():
            if e in edges:
                self.borders[e].set_color(color)
            else:
                self.borders[e].set_color(None)


class PencilFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=10, height=10, style=FrameStyles.box_frame)
        self.position = (-1, -1)

    def place_at_position(self, position, parent_position):
        row = position[0]
        col = position[1]
        self.position = position
        frame_index = row * 3 + col

        self.master.pencil_marks[frame_index] = self
        _tag_widget(self, self.find_parent(BoxFrame).binding_tag)

        number = Label(self, text=str(frame_index + 1), style=FrameStyles.pencil_label)
        number.place(relx=0.5, rely=0.5, anchor='center')
        _tag_widget(number, self.find_parent(BoxFrame).binding_tag)


class BorderFrame(Frame):
    _width = 4

    def __init__(self, master, edge):
        Frame.__init__(self, master)
        self.edge = edge

    def set_color(self, color):
        if color is None:
            self.place_forget()
            return

        self['style'] = getattr(FrameStyles, color)
        if self.edge == 'n':
            self.place(relwidth=1.0, height=BorderFrame._width, x=0, y=0, anchor='nw')
        elif self.edge == 's':
            self.place(relwidth=1.0, height=BorderFrame._width, x=0, rely=1.0, anchor='sw')
        elif self.edge == 'w':
            self.place(width=BorderFrame._width, relheight=1.0, x=0, y=0, anchor='nw')
        else: # self.edge == 'e'
            self.place(width=BorderFrame._width, relheight=1.0, relx=1.0, y=0, anchor='ne')


class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        FrameStyles.setup()

        self.clear_text = StringVar(self, "Clear")
        self.subgrids = dict()
        self.boxes = dict()
        self.active_box = None
        self.status_text = StringVar(self, "Waiting...")

        self._init_ui()
        self._init_events()

    def _init_ui(self):
        self.master.title("Sudoku Solver")
        self.pack(fill='both', expand=True)

        button_frame = Frame(self)
        button_frame.pack(fill='x', padx=5, pady=5)
        clear_button = Button(button_frame, textvariable=self.clear_text, command=self.on_clear)
        clear_button.pack(side='left')
        step_button = Button(button_frame, text=">")
        end_button = Button(button_frame, text=">>")
        end_button.pack(side='right')
        step_button.pack(side='right')

        grid_frame = Frame(self, style=FrameStyles.grid_frame)
        _build_grids(grid_frame, (0, 0), [SubGridFrame, BoxFrame])
        grid_frame.pack(fill='both', padx=5, expand=True)

        status_bar = Label(self, textvariable=self.status_text)
        status_bar.pack(fill='x', padx=5, pady=5)

    def _init_events(self):
        self.bind_all("<Key>", self.on_key)
        for box in self.boxes.values(): 
            self.bind_class(box.binding_tag, "<Button>", self.on_click)

    def on_key(self, e):
        if self.active_box is None:
            return
        if e.char in '123456789':
            self.active_box.number_text.set(e.char)
            self.active_box.set_given(True)
        else:
            self.active_box.number_text.set('')
            self.active_box.set_given(False)

    def on_click(self, e):
        box_frame = e.widget
        while box_frame is not None and not isinstance(box_frame, BoxFrame):
            box_frame = box_frame.master
        if box_frame is None:
            return
        box_frame.focus()

        if self.active_box is not None:
            self.active_box.set_borders(None)
        if self.active_box == box_frame:
            self.active_box = None
        else:
            self.active_box = box_frame
            self.active_box.set_borders('yellow')

    def on_clear(self):
        if self.active_box is not None:
            self.active_box.set_borders(None)
            self.active_box = None
        for box in self.boxes.values():
            box.number_text.set('')
            box.set_given(False)


def main():
    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
