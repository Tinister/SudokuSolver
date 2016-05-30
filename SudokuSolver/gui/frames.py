"""Holds all of the frame types that make up the GUI."""
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Button, Label
import gui.styles as styles
import gui.events as events

_subgrid_padding = 4
_box_padding = 1
_border_width = 4

def _tag_widget(self, tag):
    """Tags a widget with the given bind tag.  For use in `Widget.bind_class`.

    Args:
        self: Widget to give a bind tag to.
        tag: Tag to give.
    """
    self.bindtags((tag,) + self.bindtags())

def _build_3x3_grid(self, frame_type):
    """Builds a 3x3 grid of frames for this frame.
    For each frame created, this function will call `frame.place_at_position`.

    Args:
        self: Frame to build a grid inside of.
        frame_type: Type of frame to create the grid out of.
    Returns:
        A list of all 9 frames created in row-major ordering.
    Raises:
        AttributeError: If `frame_type` does not have a definition for `place_at_position`.
    """
    frames_created = []
    self.rowconfigure((0, 1, 2), weight=1)
    self.columnconfigure((0, 1, 2), weight=1)

    for row in (0, 1, 2):
        for col in (0, 1, 2):
            position = (row, col)
            subframe = frame_type(self)
            subframe.place_at_position(position)
            frames_created.append(subframe)
    return frames_created


class Gui(Frame, events.ModeDeferrer):
    """The most parent frame that makes up the GUI."""

    def __init__(self):
        """Construct a MainFrame with parent master.

        Args:
            master: The parent frame.
        """
        root = Tk()
        Frame.__init__(self, root)
        root.title("Sudoku Solver")
        styles.setup(root)

        self.clear_text = StringVar(self, "")
        self.step_text = StringVar(self, "")
        self.end_text = StringVar(self, "")
        self.boxes = dict()
        self.highlighted_box = None
        self.status_text = StringVar(self, "")

        self._init_ui()
        self._init_events()
        self.mode = events.InitializingMode(self)

    def _init_ui(self):
        """Initializes all the UI elements."""
        self.pack(fill='both', expand=True)

        button_frame = Frame(self)
        button_frame.pack(fill='x', padx=5, pady=5)
        clear_button = Button(button_frame, textvariable=self.clear_text, command=self.on_clear)
        clear_button.pack(side='left')
        step_button = Button(button_frame, textvariable=self.step_text, command=self.on_step)
        end_button = Button(button_frame, textvariable=self.end_text, command=self.on_end)
        end_button.pack(side='right')
        step_button.pack(side='right')

        grid_frame = Frame(self, style=styles.grid_frame)
        self.subgrids = _build_3x3_grid(grid_frame, SubGrid)
        for subgrid in self.subgrids:
            boxes = _build_3x3_grid(subgrid, Box)
            for box in boxes:
                self.boxes[box.position] = box
        grid_frame.pack(fill='both', padx=5, expand=True)

        status_bar = Label(self, textvariable=self.status_text)
        status_bar.pack(fill='x', padx=5, pady=5)

    def _init_events(self):
        """Initializes all the UI events."""
        self.bind_all("<Key>", self.on_key)
        for box in self.boxes.values():
            self.bind_class(box.binding_tag, "<Button>", lambda e, box=box: self.on_box_click(box, e))


class SubGrid(Frame):
    """Represents the larger 3x3 grid inside of the sudoku board."""

    def __init__(self, master):
        """Construct a SubGrid frame with parent master.

        Args:
            master: The parent frame.
        """
        Frame.__init__(self, master, style=styles.grid_frame)
        self.position = (0, 0)

    def place_at_position(self, position):
        """Places this frame in its parent at the given position.

        Args:
            position: Tuple of (x, y) for the position to place at.
            parent_position: Tuple of (x, y) for the position the parent is in relative to the grandparent.
        """
        row = position[0]
        col = position[1]

        self.position = position

        padx = (_subgrid_padding, 0) if col < 2 else _subgrid_padding
        pady = (_subgrid_padding, 0) if row < 2 else _subgrid_padding
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')


class Box(Frame):
    """Represents a single box (of 0-9) in the sudoku board."""
    _counter = 0

    def __init__(self, master):
        """Construct a Box frame with parent master.

        Args:
            master: The parent frame.
        """
        Frame.__init__(self, master, style=styles.box_frame)
        self.position = (0, 0)
        self.binding_tag = 'BoxFrame' + str(Box._counter)
        self.number_text = StringVar(self, '')
        Box._counter += 1

        self.borders = dict()
        for e in 'nesw':
            self.borders[e] = Border(self, e)

        self.inner_frame = Frame(self, width=30, height=30, style=styles.box_frame)
        self.pencil_marks = _build_3x3_grid(self.inner_frame, Pencil)

        self.label = Label(self.inner_frame, textvariable=self.number_text, style=styles.number_label)

        _tag_widget(self, self.binding_tag)
        _tag_widget(self.inner_frame, self.binding_tag)
        _tag_widget(self.label, self.binding_tag)
        for mark in self.pencil_marks:
            _tag_widget(mark, self.binding_tag)
            _tag_widget(mark.label, self.binding_tag)

    def place_at_position(self, position):
        """Places this frame in its parent at the given position.

        Args:
            position: Tuple of (x, y) for the position to place at.
            parent_position: Tuple of (x, y) for the position the parent is in relative to the grandparent.
        """
        row = position[0]
        col = position[1]

        parent_position = self.master.position  # master "ought to be" SubGrid
        self.position = (parent_position[0] * 3 + row, parent_position[1] * 3 + col)

        padx = (0, _box_padding) if col < 2 else 0
        pady = (0, _box_padding) if row < 2 else 0
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky='nesw')

        self.inner_frame.pack(padx=_border_width, pady=_border_width, expand=True)
        self.number = 0

    @property
    def number(self):
        """The number the box contains. Setting this value may change the box's style."""
        try:
            return int(self.number_text.get())
        except:
            return 0

    @number.setter
    def number(self, value):
        for pencil_mark in self.pencil_marks:
            pencil_mark.grid_forget()
        self['style'] = styles.box_frame
        self.inner_frame['style'] = styles.box_frame
        self.label['style'] = styles.number_label

        self.label.place(relx=0.5, rely=0.5, anchor='center')
        self.number_text.set(str(value or ' ')[0])

    @property
    def given(self):
        """The given value for this box. Setting this value may change the box's style."""
        if self['style'] != styles.given_frame:
            return 0
        else:
            return self.number

    @given.setter
    def given(self, value):
        for pencil_mark in self.pencil_marks:
            pencil_mark.grid_forget()
        self['style'] = styles.given_frame
        self.inner_frame['style'] = styles.given_frame
        self.label['style'] = styles.given_label

        self.label.place(relx=0.5, rely=0.5, anchor='center')
        self.number_text.set(str(value or ' ')[0])

    def set_pencils(self, values=0b111111111):
        """Sets the box's pencils to showing.

        Args:
            values: Which pencil marks to display.
                Bit0 set means display the '1' pencil mark, bit1 set means display the '2' pencil mark, etc.
        """
        self.label.place_forget()
        self['style'] = styles.box_frame
        self.inner_frame['style'] = styles.box_frame

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


class Pencil(Frame):
    """A smaller box (of 0-9) representing the pencil marks in a normal box."""

    def __init__(self, master):
        """Construct a Pencil frame with parent master.

        Args:
            master: The parent frame.
        """
        Frame.__init__(self, master, width=10, height=10, style=styles.box_frame)
        self.position = (0, 0)
        self.number_value = ' '
        self.number_text = StringVar(self, ' ')

        self.label = Label(self, textvariable=self.number_text, style=styles.pencil_label)
        self.label.place(relx=0.5, rely=0.5, anchor='center')

    def place_at_position(self, position):
        """Places this frame in its parent at the given position.

        Args:
            position: Tuple of (x, y) for the position to place at.
        """
        row = position[0]
        col = position[1]
        self.position = position
        frame_index = row * 3 + col
        self.number_value = str(frame_index + 1)

    def show(self, flag):
        """Show or hide the pencil frame, based on the flag.

        Args:
            flag: `True` to show this pencil mark, `False` to hide it.
        """
        self.number_text.set(self.number_value if flag else ' ')


class Border(Frame):
    """The frame element that makes up a border in a box."""

    def __init__(self, master, edge):
        """Construct a Border frame with parent master for the given edge.

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

        self['style'] = getattr(styles, color)
        if self.edge == 'n':
            self.place(relwidth=1.0, height=_border_width, x=0, y=0, anchor='nw')
        elif self.edge == 's':
            self.place(relwidth=1.0, height=_border_width, x=0, rely=1.0, anchor='sw')
        elif self.edge == 'w':
            self.place(width=_border_width, relheight=1.0, x=0, y=0, anchor='nw')
        else:  # self.edge == 'e'
            self.place(width=_border_width, relheight=1.0, relx=1.0, y=0, anchor='ne')
