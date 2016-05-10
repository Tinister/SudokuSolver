from tkinter import Tk, Text, StringVar
from tkinter.ttk import Style, Frame, Label, Button

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
        self._build_grids(grid_frame, 1)
        grid_frame.pack(fill='both', padx=5, expand=True)

        status_bar = Label(self, textvariable=self.status_text)
        status_bar.pack(fill='x', padx=5, pady=5)

    def _build_grids(self, frame, layer):
        frame.rowconfigure((0, 1, 2), weight=1)
        frame.columnconfigure((0, 1, 2), weight=1)
        style_name = None
        if layer == 2:
            style_name = 'box.TFrame'

        for row in (0, 1, 2):
            for col in (0, 1, 2):
                padx, pady = self._compute_padding(layer, row, col)

                subframe = Frame(frame, style=style_name)
                subframe.relative_position = (row, col)
                subframe.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')

                if layer == 1:
                    self._build_grids(subframe, 2)
                if layer == 2:
                    subframe.global_position = (frame.relative_position[0] * 3 + row, frame.relative_position[1] * 3 + col)
                    lbl = Label(subframe, text=str(subframe.global_position))
                    lbl.pack()

    def _compute_padding(self, layer, row, col):
        padx = 0
        pady = 0
        if layer == 1:
            if col != 2:
                padx = (0, 2)
            if row != 2:
                pady = (0, 2)
        return (padx, pady)

    def on_clear(self):
        pass


def main():
    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
