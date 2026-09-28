from client import NavierStokes2DSolver

ns = NavierStokes2DSolver(nx=12, ny=12, dt=0.05)
ns.add_force(10.0, 5.0, 5, 5)
init_div = ns.max_divergence()
ns.project(iterations=25)
final_div = ns.max_divergence()

print(f"2D Fluid Solver - Initial Max Divergence: {init_div:.4f}")
print(f"After Chorin's Projection: {final_div:.6f}")
