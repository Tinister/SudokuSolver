from tkinter import Tk, Text, StringVar
from tkinter.ttk import Frame, Label, Button
from boxframes import Styles, SubGridFrame, BoxFrame, _build_grids

class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Styles.setup()
        self._init_ui()
        self._init_events()
        self.active_box = None

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

        grid_frame = Frame(self, style=Styles.grid_frame)
        _build_grids(grid_frame, (0, 0), [SubGridFrame, BoxFrame])
        grid_frame.pack(fill='both', padx=5, expand=True)

        status_bar = Label(self, textvariable=self.status_text)
        status_bar.pack(fill='x', padx=5, pady=5)

    def _init_events(self):
        self.bind_all("<Key>", self.on_key)
        for box in BoxFrame.all.values(): 
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
        for box in BoxFrame.all.values():
            box.number_text.set('')
            box.set_given(False)


def main():
    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
