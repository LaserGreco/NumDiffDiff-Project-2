import numpy as np

class grid:
    def __init__(self, **kwargs) -> None:
        if "x" in kwargs.keys():
            assert("x0" not in kwargs.keys())
            assert("x1" not in kwargs.keys())
            assert("h" not in kwargs.keys())
            assert("N" not in kwargs.keys())
            self.x = kwargs["x"]
        elif "h" in kwargs.keys():
            assert("x0" in kwargs.keys())
            assert("x1" in kwargs.keys())
            assert("N" not in kwargs.keys())

            x0, x1, h = kwargs["x0"], kwargs["x1"], kwargs["h"]
            self.x = np.arange(x0, x1, h)

        elif "N" in kwargs.keys():
            assert("x0" in kwargs.keys())
            assert("x1" in kwargs.keys())

            x0, x1, N = kwargs["x0"], kwargs["x1"], kwargs["N"]
            self.x = np.linspace(x0, x1, N+1, endpoint=True)
        else:
            assert(True)

        self.N = len(self.x) - 1
        self.h = self.x[1] - self.x[0]

class function(grid):
    def __init__(self, **kwargs) -> None:
        super().__init__(self, **kwargs)
        self.f = None
        if "f" in kwargs.keys():
            f = kwargs["f"]
            assert len(f) == self.N + 1
            self.f = f
        
class solution(function):
    def __init__(self, a = 1, b = 1, c = 1, **kwargs) -> None:
        super().__init__(**kwargs)
        