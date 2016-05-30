"""Holds all of the event information of the GUI."""
import abc

class _Handler(metaclass=abc.ABCMeta):
    """Handles all of the events the top frame can generate."""

    @abc.abstractmethod
    def on_key(self, e):
        """Called whenever the user presses a key on their keyboard."""
        pass

    @abc.abstractmethod
    def on_box_click(self, box, e):
        """Called whenever the user clicks a box on the sudoku board."""
        pass

    @abc.abstractmethod
    def on_clear(self):
        """Called whenever the user clicks the "Clear" button."""
        pass

    @abc.abstractmethod
    def on_step(self):
        """Called whenever the user clicks the "Step" button."""
        pass

    @abc.abstractmethod
    def on_end(self):
        """Called whenever the user clicks the "End" button."""
        pass


class ModeDeferrer(_Handler):
    """Defers all event handling to a mode attribute."""
    
    def on_key(self, e):
        self.mode.on_key(e)

    def on_box_click(self, box, e):
        self.mode.on_box_click(box, e)

    def on_clear(self):
        self.mode.on_clear()

    def on_step(self):
        self.mode.on_step()

    def on_end(self):
        self.mode.on_end()


class InitializingMode(_Handler):
    """Encapsulates the behavior when the top frame is in the initializing mode."""
    _status_text = "Click on a square and type in its number, then click 'Start'."
    
    def __init__(self, top_frame):
        """Construct the initializing mode object.

        Args:
            top_frame: The top frame that will have this mode.
        """
        self.frame = top_frame
        self.frame.clear_text.set("Clear")
        self.frame.step_text.set("Start")
        self.frame.end_text.set("Solve")
        self.frame.status_text.set(InitializingMode._status_text)

    def on_key(self, e):
        """Called whenever the user presses a key on their keyboard.

        Args:
            e: Tkinter event object.
        """
        if self.frame.highlighted_box is None:
            return

        if len(e.char) > 0 and e.char in '123456789':
            self.frame.highlighted_box.given = e.char
        elif e.keysym in ['Up','Right','Down','Left']:
            x_mov = -1 if e.keysym == 'Left' else (1 if e.keysym == 'Right' else 0)
            y_mov = -1 if e.keysym == 'Up' else (1 if e.keysym == 'Down' else 0)
            new_pos = (self.frame.highlighted_box.position[0] + y_mov,
                       self.frame.highlighted_box.position[1] + x_mov)
            new_box = self.frame.boxes.get(new_pos)
            if new_box is not None:
                self.on_box_click(new_box, e)
        else:
            self.frame.highlighted_box.number = 0

    def on_box_click(self, box, e):
        """Called whenever the user clicks a box on the sudoku board.

        Args:
            box: Box frame where the event originated.
            e: Tkinter event object.
        """
        box.focus()

        if self.frame.highlighted_box is not None:
            self.frame.highlighted_box.set_borders(None)
        if self.frame.highlighted_box == box:
            self.frame.highlighted_box = None
        else:
            self.frame.highlighted_box = box
            self.frame.highlighted_box.set_borders('yellow')

    def on_clear(self):
        """Called whenever the user clicks the "Clear" button."""
        if self.frame.highlighted_box is not None:
            self.frame.highlighted_box.set_borders(None)
            self.frame.highlighted_box = None
        for box in self.frame.boxes.values():
            box.number = 0

    def on_step(self):
        """Called whenever the user clicks the "Step" button."""
        import pprint
        pprint.pprint({k: self.frame.boxes[k].number for k in self.frame.boxes.keys()})

    def on_end(self):
        """Called whenever the user clicks the "End" button."""
        pass
