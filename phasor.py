import numpy as np

pi = np.pi


class Phasor:
    def __init__(self, r, omega) -> None:
        self.r = r
        self.omega = omega
        self.theta = 0

    def update(self, dt):
        self.theta += self.omega * dt

        if self.theta > 2 * pi:
            self.theta -= 2 * pi

    def at(self):
        comp = self.r * (np.cos(self.theta) + np.sin(self.theta) * 1j)
        return np.array([np.real(comp), np.imag(comp)])

    def __repr__(self):
        return str(self.r)
