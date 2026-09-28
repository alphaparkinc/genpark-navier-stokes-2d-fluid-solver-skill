# genpark-navier-stokes-2d-fluid-solver-skill

Agent Skill implementing **2D Incompressible Navier-Stokes Fluid Dynamics** with Chorin's pressure projection method and Gauss-Seidel Poisson divergence reduction.

## Architectural Overview
```mermaid
flowchart TD
    Force["External Body Forces (F_x, F_y)"] --> Advect["Advection & Velocity Update"]
    Advect --> Div["Compute Velocity Divergence Div(u)"]
    Div --> Poisson["Gauss-Seidel Pressure Poisson Solver"]
    Poisson --> Project["Chorin Projection: u_final = u* - Grad(p)"]
    Project --> Solenoidal["Divergence-Free Velocity Field"]
```
