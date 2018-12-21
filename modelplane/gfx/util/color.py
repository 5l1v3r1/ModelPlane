import math


class Color:

    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self._color = [r, g, b, a]

    @property
    def r(self):
        return self._color[0]

    @r.setter
    def r(self, value):
        self._check_type(value)
        self._color[0] = float(value)

    @property
    def g(self):
        return self._color[1]

    @g.setter
    def g(self, value):
        self._check_type(value)
        self._color[1] = float(value)

    @property
    def b(self):
        return self._color[2]

    @b.setter
    def b(self, value):
        self._check_type(value)
        self._color[2] = float(value)

    @property
    def a(self):
        return self._color[3]

    @a.setter
    def a(self, value):
        self._check_type(value)
        self._color[3] = float(value)

    @staticmethod
    def _check_type(checkee):
        if type(checkee) not in [int, float, bool]:
            raise TypeError('Expected int or float type')

    @classmethod
    def from_hsv(cls, h, s, v):
        c = v * s
        x = c * (1 - math.fabs((h / 60.0) % 2 - 1))
        m = v - c

        rgb_prime = [(c, x, 0.0), (x, c, 0.0), (0.0, c, x), (0.0, x, c), (x, 0.0, c), (c, 0.0, x)]

        selection = rgb_prime[int(h / 60.0)]

        r = (selection[0] + m) * 255.0
        g = (selection[1] + m) * 255.0
        b = (selection[2] + m) * 255.0

        return Color(round(r), round(g), round(b), round(v * 255.0))

    def channels(self):
        return len(self._color)

    def __str__(self):
        return f'({self.r}, {self.g}, {self.b}, {self.a})'

    def __getitem__(self, item):
        if type(item) != int:
            raise TypeError('Expected integer index')
        if item not in range(len(self._color)):
            raise ValueError('Index out of bounds on Color')
        return self._color[item]
