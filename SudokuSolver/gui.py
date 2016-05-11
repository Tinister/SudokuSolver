from tkinter import Tk, Text, StringVar
from tkinter.ttk import Style, Frame, Label, Button
from boxframes import SubGridFrame, BoxFrame, _build_grids

class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Style().theme_use('default')
        Style().configure('grid.TFrame', background='#888')
        Style().configure('subgrid.TFrame', background='#888')
        Style().configure('box.TFrame', background='white')
        Style().configure('green.TFrame', background='green')
        Style().configure('red.TFrame', background='red')
        Style().configure('number.TLabel', background='white', font='Helvetica 24')
        Style().configure('pencil.TLabel', background='white', font='Helvetica 8')
        self.boxes = {}
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

        grid_frame = Frame(self, style='grid.TFrame')
        _build_grids(grid_frame, (0, 0), [SubGridFrame, BoxFrame], self)
        grid_frame.pack(fill='both', padx=5, expand=True)

        status_bar = Label(self, textvariable=self.status_text)
        status_bar.pack(fill='x', padx=5, pady=5)

    def on_clear(self):
        for box in self.boxes.values():
            box.show_pencils()


def main():
    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
