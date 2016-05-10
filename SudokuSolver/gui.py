import collections
from tkinter import Tk, Text, StringVar
from tkinter.ttk import Style, Frame, Label, Button
from boxframe import BoxFrame

class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Style().configure('box.TFrame', background='white', relief='solid', borderwidth=1)
        self._init_ui()
    
    def _init_ui(self):
        self.master.title("Sudoku Solver")
        self.pack(fill='both', expand=True)

        self.clear_text = StringVar(self, "Clear")
        self.status_text = StringVar(self, "Waiting...")

        button_frame = Frame(self)
        button_frame.pack(fill='x', padx=5, pady=5)
        clear_button = Button(button_frame, textvariable=self.clear_text, command=self.on_clear)
        clear_button.pack(side='left')
        step_button = Button(button_frame, text=">")
        end_button = Button(button_frame, text=">>")
        end_button.pack(side='right')
        step_button.pack(side='right')
        self.end_button = end_button

        grid_frame = Frame(self)
        self._build_grids(grid_frame, (0, 0),
            [self._build_grid_args(Frame, {'padx': 3, 'pady': 3}, lambda frm, pos, mwin: None),
             self._build_grid_args(BoxFrame, { }, BoxFrame.set_position)])
        grid_frame.pack(fill='both', padx=5, expand=True)

        status_bar = Label(self, textvariable=self.status_text)
        status_bar.pack(fill='x', padx=5, pady=5)

    _build_grid_args = collections.namedtuple('_build_grid_args', ['type', 'pack_args', 'set_position_func'])

    def _build_grids(self, parent_frame, parent_position, arg_list):
        if len(arg_list) <= 0:
            return
        frame_type = arg_list[0].type
        parent_frame.rowconfigure((0, 1, 2), weight=1)
        parent_frame.columnconfigure((0, 1, 2), weight=1)

        for row in (0, 1, 2):
            for col in (0, 1, 2):
                position = (parent_position[0] * 3 + row, parent_position[0] * 3 + col)

                pack_args = arg_list[0].pack_args.copy()
                self._fixup_grid_args(row, col, pack_args)

                subframe = frame_type(parent_frame)
                subframe.grid(**pack_args)

                arg_list[0].set_position_func(subframe, position, self)
                self._build_grids(subframe, position, arg_list[1:])

    def _fixup_grid_args(self, row, col, kwargs):
        kwargs['row'] = row
        kwargs['column'] = col
        kwargs['sticky'] = 'nesw'
        if 'padx' in kwargs:
            kwargs['padx'] = (0, kwargs['padx']) if col < 2 else 0
        if 'pady' in kwargs:
            kwargs['pady'] = (0, kwargs['pady']) if row < 2 else 0

    def on_clear(self):
        pass


def main():
    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
