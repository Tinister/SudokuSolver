"""Contains a GUI interface for the sudoku module"""
from tkinter import Tk, Text, StringVar
from tkinter.ttk import Style, Widget, Frame, Label, Button


def _get_number(text):
    """Converts text to a number.  Returns 0 if the text is not a valid number.

    Args:
        text: Text to convert to a number.
    """
    try:
        return int(text)
    except:
        return 0


def _build_grids(parent_frame, parent_position, frame_type):
    """Builds a 3x3 grid of frames in the given parent frame.
    For each frame created, this function will call `frame.place_at_position`.

    Args:
        parent_frame: Frame to build a grid inside of.
        parent_position: Tuple of (x, y) for the parent's position in *its* parent.
        frame_type: Type of frame to create the grid out of.
    Raises:
        AttributeError: If `frame_type` does not have a definition for `place_at_position`.
    """
    parent_frame.rowconfigure((0, 1, 2), weight=1)
    parent_frame.columnconfigure((0, 1, 2), weight=1)

    for row in (0, 1, 2):
        for col in (0, 1, 2):
            position = (row, col)
            subframe = frame_type(parent_frame)
            subframe.place_at_position(position, parent_position)


def _tag_widget(widget, tag):
    """Tags a widget with the given bind tag.  For use in `Widget.bind_class`.

    Args:
        widget: Widget to give a bind tag to.
        tag: Tag to give.
    """
    widget.bindtags((tag,) + widget.bindtags())


def _find_parent(self, type_name):
    """Walks up the widget's parent chain until it finds a widget of the given type.

    Args:
        type_name: Type to look for.
    Returns:
        The first widget walking up the parent chain of the given type,
        or `None` if no such parent was found.
    """
    curr = self
    while True:
        if curr is None or type(curr) is type_name:
            return curr
        curr = curr.master

Widget.find_parent = _find_parent


class FrameStyles(object):
    """Class that groups all the custom styles defined."""
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
        """Sets up all the custom styles."""
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
    """Represents the larger 3x3 grid inside of the sudoku board."""
    _padding = 4

    def __init__(self, master):
        """Construct a PencilFrame with parent master.

        Args:
            master: The parent frame.
        """
        Frame.__init__(self, master, style=FrameStyles.grid_frame)
        self.position = (-1, -1)

    def place_at_position(self, position, parent_position):
        """Places the SubGridFrame in its parent at the given position.

        Args:
            position: Tuple of (x, y) for the position to place at.
            parent_position: Tuple of (x, y) for the position the parent is in relative to the grandparent.
        """
        row = position[0]
        col = position[1]

        self.position = position
        self.find_parent(MainFrame).subgrids[self.position] = self
        _build_grids(self, position, BoxFrame)

        padx = (SubGridFrame._padding, 0) if col < 2 else SubGridFrame._padding
        pady = (SubGridFrame._padding, 0) if row < 2 else SubGridFrame._padding
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')


class BoxFrame(Frame):
    """Represents a single box (of 0-9) in the sudoku board."""
    _counter = 0
    _padding = 1

    def __init__(self, master):
        """Construct a PencilFrame with parent master.

        Args:
            master: The parent frame.
        """
        Frame.__init__(self, master, style=FrameStyles.box_frame)
        self.position = (-1, -1)
        self.binding_tag = 'BoxFrame' + str(BoxFrame._counter)
        self.number_text = StringVar(self, '')
        BoxFrame._counter += 1

        self.borders = dict()
        for e in 'nesw':
            self.borders[e] = BorderFrame(self, e)

        self.content_frame = Frame(self, width=30, height=30, style=FrameStyles.box_frame)

        self.pencil_marks = [None] * 9
        _build_grids(self.content_frame, (0, 0), PencilFrame)

        self.number = Label(self.content_frame, textvariable=self.number_text, style=FrameStyles.number_label)

        _tag_widget(self, self.binding_tag)
        _tag_widget(self.content_frame, self.binding_tag)
        _tag_widget(self.number, self.binding_tag)

    def place_at_position(self, position, parent_position):
        """Places the BoxFrame in its parent at the given position.

        Args:
            position: Tuple of (x, y) for the position to place at.
            parent_position: Tuple of (x, y) for the position the parent is in relative to the grandparent.
        """
        row = position[0]
        col = position[1]

        self.position = (parent_position[0] * 3 + row, parent_position[1] * 3 + col)
        self.find_parent(MainFrame).boxes[self.position] = self

        padx = (0, BoxFrame._padding) if col < 2 else 0
        pady = (0, BoxFrame._padding) if row < 2 else 0
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')

        self.content_frame.pack(padx=BorderFrame._width, pady=BorderFrame._width, expand=True)
        self.set_number('')

    def get_number(self):
        return _get_number(self.number_text.get())

    def set_number(self, value=None):
        """Sets the box's number to showing.

        Args:
            value: What number to display.  Omitting this argument means keeping the current number.
        """
        value = self.number_text.get() if value is None else value

        for pencil_mark in self.pencil_marks:
            pencil_mark.grid_forget()
        self['style'] = FrameStyles.box_frame
        self.content_frame['style'] = FrameStyles.box_frame
        self.number['style'] = FrameStyles.number_label

        self.number.place(relx=0.5, rely=0.5, anchor='center')
        self.number_text.set(str(value or ' ')[0])

    def set_given(self, value=None):
        """Sets the box to use the "given number" style.

        Args:
            value: What number to display.  Omitting this argument means keeping the current number.
        """
        value = self.number_text.get() if value is None else value

        for pencil_mark in self.pencil_marks:
            pencil_mark.grid_forget()
        self['style'] = FrameStyles.given_frame
        self.content_frame['style'] = FrameStyles.given_frame
        self.number['style'] = FrameStyles.given_label

        self.number.place(relx=0.5, rely=0.5, anchor='center')
        self.number_text.set(str(value or ' ')[0])

    def set_pencils(self, values=0b111111111):
        """Sets the box's pencils to showing.

        Args:
            values: Which pencil marks to display.
                Bit0 set means display the '1' pencil mark, bit1 set means display the '2' pencil mark, etc.
        """
        self.number.place_forget()
        self['style'] = FrameStyles.box_frame
        self.content_frame['style'] = FrameStyles.box_frame

        for i in range(0, 9):
            pencil_mark = self.pencil_marks[i]
            pencil_mark.show(values & (1 << i))
            pencil_mark.grid(row=pencil_mark.position[0], column=pencil_mark.position[1], sticky='nesw')

    def set_borders(self, color, edges='nesw'):
        """Sets the borders on this box frame.

        Args:
            color: Color of borders to set, or `None` to hide the borders.
            edges: A subset of 'nesw' for which borders to show.
        """
        for e in self.borders.keys():
            if e in edges:
                self.borders[e].set_color(color)
            else:
                self.borders[e].set_color(None)


class PencilFrame(Frame):
    """A smaller box (of 0-9) representing the pencil marks in a normal box."""

    def __init__(self, master):
        """Construct a PencilFrame with parent master.

        Args:
            master: The parent frame.
        """
        Frame.__init__(self, master, width=10, height=10, style=FrameStyles.box_frame)
        self.position = (-1, -1)
        self.number_value = ' '
        self.number_text = StringVar(self, ' ')

        number = Label(self, textvariable=self.number_text, style=FrameStyles.pencil_label)
        number.place(relx=0.5, rely=0.5, anchor='center')

        _tag_widget(self, self.find_parent(BoxFrame).binding_tag)
        _tag_widget(number, self.find_parent(BoxFrame).binding_tag)


    def place_at_position(self, position, parent_position):
        """Places the PencilFrame in its parent at the given position.

        Args:
            position: Tuple of (x, y) for the position to place at.
            parent_position: Tuple of (x, y) for the position the parent is in relative to the grandparent.
        """
        row = position[0]
        col = position[1]
        self.position = position
        frame_index = row * 3 + col
        self.number_value = str(frame_index + 1)

        self.find_parent(BoxFrame).pencil_marks[frame_index] = self

    def show(self, flag):
        """Show or hide the pencil frame, based on the flag.

        Args:
            flag: `True` to show this pencil mark, `False` to hide it.
        """
        self.number_text.set(self.number_value if flag else ' ')


class BorderFrame(Frame):
    """The frame element that makes up a border in the a box."""
    _width = 4

    def __init__(self, master, edge):
        """Construct a BorderFrame with parent master for the given edge.

        Args:
            master: The parent frame.
            edge: One of 'nesw' for which edge this frame should attach to.
        """
        Frame.__init__(self, master)
        self.edge = edge

    def set_color(self, color):
        """Set the color of this border.

        Args:
            color: The color to set this border to.
        """
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
        else:  # self.edge == 'e'
            self.place(width=BorderFrame._width, relheight=1.0, relx=1.0, y=0, anchor='ne')


class MainFrame(Frame):
    """The most parent frame that makes up the GUI."""

    def __init__(self, master):
        """Construct a MainFrame with parent master.

        Args:
            master: The parent frame.
        """
        Frame.__init__(self, master)
        FrameStyles.setup()

        self.clear_text = StringVar(self, "")
        self.step_text = StringVar(self, "")
        self.end_text = StringVar(self, "")
        self.subgrids = dict()
        self.boxes = dict()
        self.highlighted_box = None
        self.status_text = StringVar(self, "")

        self._init_ui()
        self._init_events()
        self.mode = InitializingMode(self)

    def _init_ui(self):
        """Initializes all the UI elements."""
        self.master.title("Sudoku Solver")
        self.pack(fill='both', expand=True)

        button_frame = Frame(self)
        button_frame.pack(fill='x', padx=5, pady=5)
        clear_button = Button(button_frame, textvariable=self.clear_text, command=self.on_clear)
        clear_button.pack(side='left')
        step_button = Button(button_frame, textvariable=self.step_text, command=self.on_step)
        end_button = Button(button_frame, textvariable=self.end_text, command=self.on_end)
        end_button.pack(side='right')
        step_button.pack(side='right')

        grid_frame = Frame(self, style=FrameStyles.grid_frame)
        _build_grids(grid_frame, (0, 0), SubGridFrame)
        grid_frame.pack(fill='both', padx=5, expand=True)

        status_bar = Label(self, textvariable=self.status_text)
        status_bar.pack(fill='x', padx=5, pady=5)

    def _init_events(self):
        """Initializes all the UI events."""
        self.bind_all("<Key>", self.on_key)
        for box in self.boxes.values():
            self.bind_class(box.binding_tag, "<Button>", self.on_click)

    def on_key(self, e):
        """Called whenever the user presses a key on their keyboard."""
        self.mode.on_key(e)

    def on_click(self, e):
        """Called whenever the user clicks on the sudoku board."""
        self.mode.on_click(e)

    def on_clear(self):
        """Called whenever the user clicks the "Clear" button."""
        self.mode.on_clear()

    def on_step(self):
        """Called whenever the user clicks the "Step" button."""
        self.mode.on_step()

    def on_end(self):
        """Called whenever the user clicks the "End" button."""
        self.mode.on_end()


class InitializingMode(object):
    """Encapsulates the behavior when MainFrame is in the initializing mode."""
    _status_text = "Click on a square and type in its number, then click 'Start'."
    
    def __init__(self, main):
        """Construct the initializing mode object.

        Args:
            main: The MainFrame object that will have this mode.
        """
        self.main = main
        self.main.clear_text.set("Clear")
        self.main.step_text.set("Start")
        self.main.end_text.set("Solve")
        self.main.status_text.set(InitializingMode._status_text)

    def on_key(self, e):
        """Called whenever the user presses a key on their keyboard.

        Args:
            e: Tkinter event object.
        """
        if self.main.highlighted_box is None:
            return

        if len(e.char) > 0 and e.char in '123456789':
            self.main.highlighted_box.set_given(e.char)
        elif e.keysym in ['Up','Right','Down','Left']:
            x_mov = -1 if e.keysym == 'Left' else (1 if e.keysym == 'Right' else 0)
            y_mov = -1 if e.keysym == 'Up' else (1 if e.keysym == 'Down' else 0)
            new_pos = (self.main.highlighted_box.position[0] + y_mov,
                       self.main.highlighted_box.position[1] + x_mov)
            new_box = self.main.boxes.get(new_pos)
            if new_box is not None:
                e.widget = new_box
                self.on_click(e)
        else:
            self.main.highlighted_box.set_number('')

    def on_click(self, e):
        """Called whenever the user clicks on the sudoku board.

        Args:
            e: Tkinter event object.
        """
        box_frame = e.widget.find_parent(BoxFrame)
        if box_frame is None:
            return
        box_frame.focus()

        if self.main.highlighted_box is not None:
            self.main.highlighted_box.set_borders(None)
        if self.main.highlighted_box == box_frame:
            self.main.highlighted_box = None
        else:
            self.main.highlighted_box = box_frame
            self.main.highlighted_box.set_borders('yellow')

    def on_clear(self):
        """Called whenever the user clicks the "Clear" button."""
        if self.main.highlighted_box is not None:
            self.main.highlighted_box.set_borders(None)
            self.main.highlighted_box = None
        for box in self.main.boxes.values():
            box.set_number('')

    def on_step(self):
        """Called whenever the user clicks the "Step" button."""
        import pprint
        pprint.pprint({k: self.main.boxes[k].get_number() for k in self.main.boxes.keys()})

    def on_end(self):
        """Called whenever the user clicks the "End" button."""
        pass


def main():
    """Entry point for creating a GUI frame."""
    root = Tk()
    app = MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
