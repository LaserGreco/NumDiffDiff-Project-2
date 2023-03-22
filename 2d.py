from FEM import *

if __name__ == "__main__":
    def w1_exact(x):
        return np.where(x < 1/2, 2*x, 2*(1-x))

    def w1_f(x, a=1, b=1, c=1):
        return np.where(x < 1/2, 2*b+2*c*x, -2*b+2*c*(1-x))
    
    w1_disc = np.array([
        [4, 1/2]
    ])

    u = solve_system(w1_f, exact=w1_exact, N=100, disc=w1_disc)

    u.plot_comparison()
    plt.legend()
    plt.xlabel('x')

    plt.show()

    ax = plt.subplot()

    u.plot_error(ax=ax)
    ax.legend()
    ax.set_xlabel('x')

    plt.show()

    plot_convergence(w1_f, w1_exact, disc=w1_disc, title="Convergence of solver")