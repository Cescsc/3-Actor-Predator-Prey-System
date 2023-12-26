import tkinter as tk


class _Grid(tk.Canvas):
    """
    2D cellular grid for the cellular automaton.
    """

    def __init__(self, master, width, bg, height, grid_len, env_size, hide_grid=True, **kwargs):
        """Initializes the grid."""
        super().__init__(master, width=width, bg=bg, height=height, **kwargs)
        self.master = master

        self.width = width
        self.height = height
        self.grid_len = grid_len
        self.env_size = env_size

        if not hide_grid:
            self.create_grid(grid_len=self.grid_len)

        self.pack()

    def create_grid(self, grid_len=20):
        self.delete('grid_line')  # Will only remove the grid_line

        for i in range(0, self.width, self.grid_len):
            self.create_line([(i, 0), (i, self.height)], tag='grid_line', fill="grey")

        for i in range(0, self.height, self.grid_len):
            self.create_line([(0, i), (self.width, i)], tag='grid_line', fill="grey")

    def _blit_circle(self, obj):
        es = self.env_size
        r = int(self.grid_len * obj.size)
        x0 = self.width * 1/es * obj.pos[0] - r
        y0 = self.height * 1/es * obj.pos[1] - r
        x1 = self.width * 1/es * obj.pos[0] + r
        y1 = self.height * 1/es * obj.pos[1] + r
        self.create_oval(x0, y0, x1, y1, fill=obj.color)

    def clear(self):
        self.delete("all")

    def update(self):
        self.master.update()

    def quit(self):
        self.master.quit()