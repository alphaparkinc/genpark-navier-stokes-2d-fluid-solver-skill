"""2D Incompressible Navier-Stokes Fluid Solver.
100% Python Standard Library.
"""

class NavierStokes2DSolver:
    """2D Incompressible Navier-Stokes grid solver with pressure Poisson projection."""
    def __init__(self, nx=16, ny=16, dt=0.1, visc=0.001):
        self.nx = nx
        self.ny = ny
        self.dt = dt
        self.visc = visc
        self.u = [[0.0] * ny for _ in range(nx)]
        self.v = [[0.0] * ny for _ in range(nx)]
        self.p = [[0.0] * ny for _ in range(nx)]

    def add_force(self, fx, fy, x, y):
        if 0 <= x < self.nx and 0 <= y < self.ny:
            self.u[x][y] += fx * self.dt
            self.v[x][y] += fy * self.dt

    def project(self, iterations=20):
        nx, ny = self.nx, self.ny
        div = [[0.0] * ny for _ in range(nx)]
        p = [[0.0] * ny for _ in range(nx)]

        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                div[i][j] = -0.5 * ((self.u[i+1][j] - self.u[i-1][j]) + (self.v[i][j+1] - self.v[i][j-1]))

        for _ in range(iterations):
            for i in range(1, nx - 1):
                for j in range(1, ny - 1):
                    p[i][j] = (div[i][j] + p[i-1][j] + p[i+1][j] + p[i][j-1] + p[i][j+1]) / 4.0

        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                self.u[i][j] -= 0.5 * (p[i+1][j] - p[i-1][j])
                self.v[i][j] -= 0.5 * (p[i][j+1] - p[i][j-1])

        self.p = p

    def max_divergence(self):
        max_div = 0.0
        for i in range(1, self.nx - 1):
            for j in range(1, self.ny - 1):
                d = abs(0.5 * ((self.u[i+1][j] - self.u[i-1][j]) + (self.v[i][j+1] - self.v[i][j-1])))
                if d > max_div:
                    max_div = d
        return max_div
