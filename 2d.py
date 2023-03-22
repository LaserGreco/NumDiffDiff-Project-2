from FEM import *

if __name__ == "__main__":
    def exact(x):
        # return x*(1 - x) / 2
        return np.sin(3*np.pi*x)

    def f(x):
        # return (-x**2 - x + 3)/2
        return 3*np.pi*np.cos(3*np.pi*x) + np.sin(3*np.pi*x) + (3*np.pi)**2 * np.sin(3*np.pi*x)


    # u = solve_system(f, exact=exact, N=100)

    # u.plot_comparison()
    # plt.legend()
    # plt.xlabel('x')

    # plt.show()

    # ax = plt.subplot()

    # u.plot_error(ax=ax)
    # ax.legend()
    # ax.set_xlabel('x')

    # plt.show()

    plot_convergence(f, exact, title="Convergence of solver")