import pyglet
from pyglet.shapes import BorderedRectangle, Circle
from pyglet.window import Window


class MainWindow(Window):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_location(100, 100)
        self.batch = pyglet.graphics.Batch()

        self.d = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        self.rect = [
            [
                BorderedRectangle(j * 100, i * 100, 100, 100, batch=self.batch)
                for j in range(len(self.d[i]))
            ]
            for i in range(len(self.d))
        ]

        self.rc = []
        self.mode = 0

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_update(self, dt, _dz):
        pass

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.mode == 0:
            self.d[int(y / 100)][int(x / 100)] = (
                self.d[int(y / 100)][int(x / 100)] + 1
            ) % 2

            self.rect[int(y / 100)][int(x / 100)].color = [
                (255, 255, 255),
                (0, 0, 0),
            ][self.d[int(y / 100)][int(x / 100)]]
        else:
            print(f"({round(x / 100)}, {round(y / 100)}),")
            self.rc.append(
                Circle(
                    100 * round(x / 100),
                    100 * round(y / 100),
                    10,
                    color=(255, 0, 0),
                    batch=self.batch,
                )
            )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == 112:
            self.mode = (self.mode + 1) % 2
            self.rc.clear()
            print("--------------------")


if __name__ == "__main__":
    win = MainWindow(400, 500)
    pyglet.clock.schedule(win.on_update, 1 / 60)
    pyglet.app.run()
