import numpy as np

class Grid:
    def __init__(self, **kwargs) -> None:
        if "x" in kwargs.keys() or "grid" in kwargs.keys():
            assert("x0" not in kwargs.keys())
            assert("x1" not in kwargs.keys())
            assert("h" not in kwargs.keys())
            assert("N" not in kwargs.keys())
            if "x" in kwargs.keys():
                assert "grid" not in kwargs.keys()

                x = kwargs["x"]
            else:
                x = kwargs["grid"].x
        else:
            if "x0" in kwargs.keys():
                x0 = kwargs["x0"]
            else:
                x0 = 0
            if "x1" in kwargs.keys():
                x1 = kwargs["x1"]
            else:
                x1 = 1
            assert x0 < x1
            if "h" in kwargs.keys():
                assert("x0" in kwargs.keys())
                assert("x1" in kwargs.keys())
                assert("N" not in kwargs.keys())

                x0, x1, h = kwargs["x0"], kwargs["x1"], kwargs["h"]
                x = np.arange(x0, x1, h)
            elif "N" in kwargs.keys():
                N = kwargs["N"]
                x = np.linspace(x0, x1, N+1, endpoint=True)
            else:
                x = np.linspace(0, 1, 50+1, endpoint=True)

        self.x = x
        self.N = len(self.x) - 1
        self.h = self.x[1:] - self.x[:-1]

class Function(Grid):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.f = None
        if "f" in kwargs.keys():
            f = kwargs["f"]
            if callable(f):
                f = f(self.x)
            assert len(f) == self.N + 1
            self.f = f
        else:
            self.f = np.zeros_like(self.x)
    
    def get_F(self) -> np.ndarray:
        F = self.f[1:-1] * self.h[1:]

        return F
        
class Solver(Grid):
    def __init__(self, a = 1, b = 1, c = 1, **kwargs) -> None:
        super().__init__(**kwargs)
        self.a = a
        self.b = b
        self.c = c

        Ak = lambda i: a * np.array([
                            [1, -1],
                            [-1, 1]
                        ]) / self.h[i]
        Bk = lambda i: b * np.array([
                            [-1/2, 1/2],
                            [-1/2, 1/2]
                        ])
        Ck = lambda i: c * np.array([
                            [1/3, 1/6],
                            [1/6, 1/3]
                        ]) * self.h[i]

        M = np.zeros((self.N+1, self.N+1))

        for i in range(self.N):
            M[i:i+2, i:i+2] += Ak(i) + Bk(i) + Ck(i)
        self.M = M[1:-1, 1:-1]

    def solve(self, f) -> Function:
        if callable(f):
            f = Function(f=f(self.x), grid=self)
        F = f.get_F()
        u = Function(grid=self)
        u.f[1:-1] = np.linalg.solve(self.M, F)
        return u
    

def solve_system(f, **kwargs) -> Function:
    if "solver" in kwargs.keys():
        assert "grid" not in kwargs.keys()
        solver = kwargs["solver"]
    else:
        solver = Solver(**kwargs)

    return solver.solve(f)

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def g(x):
        return x*(1 - x) / 2

    def f(x):
        return (-x**2 - x + 3)/2


    u = solve_system(f)

    x = u.x

    plt.plot(x, u.f, x, g(x),'o')
    plt.legend(['Numerical','Exact'])
    plt.xlabel('x')

    plt.show()

    plt.plot(x, u.f-g(x))
    plt.legend("error")
    plt.xlabel('x')

    plt.show()