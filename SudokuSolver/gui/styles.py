"""Module that groups all the custom styles defined."""
from tkinter.ttk import Style

grid_frame = 'grid.TFrame'
box_frame = 'box.TFrame'
given_frame = 'given.TFrame'
number_label = 'number.TLabel'
given_label = 'given.TLabel'
pencil_label = 'pencil.TLabel'
green = 'green.TFrame'
red = 'red.TFrame'
yellow = 'yellow.TFrame'

def setup(tk):
    """Sets up all the custom styles.
    
    Args:
        Toplevel Tk instance.
    """
    s = Style(tk)
    s.theme_use('default')
    s.configure(grid_frame, background='#888')
    s.configure(box_frame, background='white')
    s.configure(given_frame, background='#ddd')
    s.configure(number_label, background='white', font='Helvetica 24')
    s.configure(given_label, background='#ddd', font='Helvetica 24 bold')
    s.configure(pencil_label, background='white', font='Helvetica 8')
    s.configure(green, background='green')
    s.configure(red, background='red')
    s.configure(yellow, background='yellow')
