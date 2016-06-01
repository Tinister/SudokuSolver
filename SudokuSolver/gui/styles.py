"""Module that groups all the custom styles defined."""
from tkinter.ttk import Style

GRID_FRAME = 'grid.TFrame'
BOX_FRAME = 'box.TFrame'
GIVEN_FRAME = 'given.TFrame'
NUMBER_LABEL = 'number.TLabel'
GIVEN_LABEL = 'given.TLabel'
PENCIL_LABEL = 'pencil.TLabel'
GREEN = 'green.TFrame'
RED = 'red.TFrame'
YELLOW = 'yellow.TFrame'

def setup(tk_instance):
    """Sets up all the custom styles.

    Args:
        Toplevel Tk instance.
    """
    style = Style(tk_instance)
    style.theme_use('default')
    style.configure(GRID_FRAME, background='#888')
    style.configure(BOX_FRAME, background='white')
    style.configure(GIVEN_FRAME, background='#ddd')
    style.configure(NUMBER_LABEL, background='white', font='Helvetica 24')
    style.configure(GIVEN_LABEL, background='#ddd', font='Helvetica 24 bold')
    style.configure(PENCIL_LABEL, background='white', font='Helvetica 8')
    style.configure(GREEN, background='green')
    style.configure(RED, background='red')
    style.configure(YELLOW, background='yellow')
