import tkinter as tk

WIDTH = 1000
HEIGHT = 1000

class Grid(tk.Canvas):
    """
    2D cellular grid for the cellular automaton. Handles all the graphics.
    """

    def __init__(self, bg, env_size, hide_grid=False, **kwargs):
        """Initializes the grid."""
        self.master = tk.Tk()
        super().__init__(self.master, width=WIDTH, bg=bg, height=HEIGHT, **kwargs)

        self.env_size = env_size
        self.gridlen = WIDTH//env_size

        if not hide_grid:
            self.create_grid()

        self.pack()

    def create_grid(self):
        self.delete('grid_line')

        for i in range(0, WIDTH, self.gridlen):
            self.create_line([(i, 0), (i, HEIGHT)], tag='grid_line', fill="grey")

        for i in range(0, HEIGHT, self.gridlen):
            self.create_line([(0, i), (WIDTH, i)], tag='grid_line', fill="grey")

    def blit_rect(self, obj):
        topleft_x = obj.pos[0]*self.gridlen
        topleft_y = obj.pos[1]*self.gridlen
        botright_x = topleft_x + self.gridlen
        botright_y = topleft_y + self.gridlen
        self.create_rectangle(topleft_x, topleft_y, botright_x, botright_y, fill=obj.color)

    def clear(self):
        self.delete("all")
        self.create_grid()

    def update(self):
        self.master.update()

    def quit(self):
        self.master.quit()
