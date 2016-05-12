from tkinter import Tk, Text, StringVar
from tkinter.ttk import Frame, Label, Button
from boxframes import Styles, SubGridFrame, BoxFrame, _build_grids

class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Styles.setup()
        self._init_ui()
        self.foo = True
    
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

        grid_frame = Frame(self, style=Styles.grid_frame)
        _build_grids(grid_frame, (0, 0), [SubGridFrame, BoxFrame])
        grid_frame.pack(fill='both', padx=5, expand=True)

        status_bar = Label(self, textvariable=self.status_text)
        status_bar.pack(fill='x', padx=5, pady=5)

    def on_clear(self):
        for box in BoxFrame.all.values():
            box.set_given(self.foo)
        self.foo = not self.foo


def main():
    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
