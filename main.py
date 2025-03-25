from typing import List

import numpy as np
import pyglet
from pyglet.shapes import Circle, Line
from pyglet.window import Window

from convert import convert_to_phasor_list
from glyphs import glyph_roll_num


class MainWindow(Window):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_location(100, 100)
        self.batch = pyglet.graphics.Batch()
        self.set_caption("EE1101")
        self.p = convert_to_phasor_list(glyph_roll_num, T=30, max_dlen=460)
        self.phasor_lines = [
            Line(0, 0, 0, 0, batch=self.batch) for _ in range(len(self.p))
        ]
        self.c = Circle(0, 0, 5, batch=self.batch)
        self.lcoord = None
        self.fc = 0

        self.lines: List[Line] = []
        self.neon_lines: List[Line] = []

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_update(self, dt, _dz):
        for i in range(len(self.p)):
            self.p[i].update(dt)

        i = 0
        if self.fc % 2 == 0:
            while i < len(self.lines):
                r, g, b, a = self.lines[i].color
                if a > 50:
                    a -= 1
                    self.lines[i].color = (r, g, b, a)
                    r1, g1, b1, a1 = self.neon_lines[i].color
                    a1 -= 1
                    self.neon_lines[i].color = (r1, g1, b1, a1)
                i += 1

        self.fc += 1

        if len(self.lines) > 1750:
            del self.lines[0]
            del self.neon_lines[0]

        coord = np.array([self.width / 2, self.height / 2 - 100])
        for i in range(len(self.p)):
            c1 = coord + self.p[i].at()
            self.phasor_lines[i].x = coord[0]
            self.phasor_lines[i].y = coord[1]
            self.phasor_lines[i].x2 = c1[0]
            self.phasor_lines[i].y2 = c1[1]

            coord = c1
        self.c.x = coord[0]
        self.c.y = coord[1]

        if self.lcoord is not None:
            self.neon_lines.append(
                Line(
                    self.lcoord[0],
                    self.lcoord[1],
                    coord[0],
                    coord[1],
                    color=(0, 0, 155),
                    batch=self.batch,
                    thickness=15,
                )
            )

            self.lines.append(
                Line(
                    self.lcoord[0],
                    self.lcoord[1],
                    coord[0],
                    coord[1],
                    color=(0, 155, 255),
                    batch=self.batch,
                )
            )

        self.lcoord = coord


if __name__ == "__main__":
    win = MainWindow(1920, 1080)
    pyglet.clock.schedule(win.on_update, 1 / 60)
    pyglet.app.run()
