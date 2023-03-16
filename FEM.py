import numpy as np
import matplotlib.pyplot as plt

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
    def __init__(self, func = None, **kwargs) -> None:
        super().__init__(**kwargs)
        if func is not None:
            assert isinstance(func, Function)
            self.f = func.f.copy()
            self.x = func.x
            self.N = func.N
        else:
            if "f" in kwargs.keys():
                f = kwargs["f"]
                if callable(f):
                    f = f(self.x)
                assert len(f) == self.N + 1
                self.f = f.copy()
            else:
                self.f = np.zeros_like(self.x)

    def __add__(self, other):
        out = Function(self)
        if isinstance(other, Function):
            out.f += other.f
        else:   
            out.f += other
        return out
    
    def __sub__(self, other):
        if isinstance(other, Function):
            f = other.f
        else:
            f = other
        return self + (-f)
    
    def get_F(self) -> np.ndarray:
        F = self.f[1:-1] * self.h[1:]

        return F
    
    def plot(self, *args, **kwargs) -> None:
        if "ax" in kwargs.keys():
            ax = kwargs["ax"]
            kwargs.pop("ax")
            ax.plot(self.x, self.f, *args, **kwargs)
        else:
            plt.plot(self.x, self.f, *args, **kwargs)

class Solution(Function):
    def __init__(self, exact=None, func=None, **kwargs) -> None:
        super().__init__(func, **kwargs)
        self.set_exact(exact)

    def set_exact(self, exact) -> None:
        if callable(exact):
            exact = Function(f=exact, grid=self)
        elif isinstance(exact, np.ndarray):
            assert len(exact) == self.N+1
            exact = Function(f=exact, grid=self)
        elif isinstance(exact, Function):
            assert (exact.x == self.x).all()
        self.exact = exact

    def get_error(self) -> Function:
        assert self.exact is not None

        return self - self.exact
    
    def plot_comparison(self, *args, **kwargs) -> None:
        assert self.exact is not None
        assert "label" not in kwargs.keys()
        self.plot(label="Numerical", *args, **kwargs)
        self.exact.plot("o", *args, label="Exact", **kwargs)

    def plot_error(self, *args, **kwargs) -> None:
        assert self.exact is not None
        if "label" not in kwargs.keys():
            kwargs["label"] = "Error"
        self.get_error().plot(*args, **kwargs)
        
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

    def solve(self, f, exact=None) -> Function:
        if callable(f):
            f = Function(f=f(self.x), grid=self)
        F = f.get_F()
        u = Solution(exact=exact, grid=self)
        u.f[1:-1] = np.linalg.solve(self.M, F)
        return u
    

def solve_system(f, exact=None, **kwargs) -> Function:
    if "solver" in kwargs.keys():
        assert "grid" not in kwargs.keys()
        solver = kwargs["solver"]
    else:
        solver = Solver(**kwargs)

    return solver.solve(f, exact)

if __name__ == "__main__":
    def exact(x):
        # return x*(1 - x) / 2
        return np.sin(3*np.pi*x)

    def f(x):
        # return (-x**2 - x + 3)/2
        return 3*np.pi*np.cos(3*np.pi*x) + np.sin(3*np.pi*x) + (3*np.pi)**2 * np.sin(3*np.pi*x)


    u = solve_system(f, exact=exact)
    # u.set_exact(g)

    u.plot_comparison()
    plt.legend()
    plt.xlabel('x')

    plt.show()

    ax = plt.subplot()

    # (u-u_exact).plot(ax=ax, label="error")
    u.plot_error(ax=ax)
    ax.legend()
    ax.set_xlabel('x')

    plt.show()