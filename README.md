# Orifice-plate-ISO-5167

CFD validation of an orifice plate discharge coefficient (Cd) against ISO 5167-2 (Reader-Harris/Gallagher) for an oil & gas water-injection metering case. 2D axisymmetric RANS in ANSYS Fluent, mesh independence study with GCI, 4" line, β = 0.6, flange taps, Re 5×10⁴–5×10⁵.

> **Status:** 🚧 Work in progress — Phase 1 (geometry, mesh and mesh independence) complete. A transient start-up run is also done. Next: Phase 2, Cd across the Reynolds range.

## The question

Orifice plates are the workhorse of flow metering in oil & gas: no moving parts, suitable for high pressure, and standardized. If a plate is built and installed according to ISO 5167-2, its discharge coefficient is known from the Reader-Harris/Gallagher (RHG) correlation without calibration.

**How well does a RANS CFD model reproduce that discharge coefficient across the operating range?**

## Case study (fictitious)

| Item | Value |
|---|---|
| Service | Water-injection line metering |
| Fluid | Water at 20 °C (ρ = 998.2 kg/m³, μ = 1.002×10⁻³ Pa·s), incompressible, single-phase |
| Pipe | 4" Sch 40, D = 102.3 mm |
| Orifice | Concentric, square-edged, β = 0.6 (d = 61.38 mm) |
| Plate | E = 3 mm, e = 1.5 mm, 45° downstream bevel |
| Pressure taps | Flange taps, 25.4 mm from each plate face |
| Pipe Reynolds number | 5×10⁴, 1×10⁵, 3×10⁵, 5×10⁵ (mean velocity 0.49–4.91 m/s) |

All parameters are within the ISO 5167-2:2003 limits of use for flange tappings. Since Cd depends only on β and Re for a given geometry, the results apply to any Newtonian single-phase liquid at the same Reynolds number.

## Method

- **Domain:** 2D axisymmetric fluid region, 10D upstream and 20D downstream of the plate (see [`geometry/`](geometry/)).
- **Solver:** ANSYS Fluent 2026 R1 (Student), pressure-based coupled solver, second-order spatial discretization, steady state.
- **Turbulence:** k-ω SST (baseline), with a second model for sensitivity.
- **Near-wall resolution:** inflation on the pipe and plate walls only, first layer 0.02 mm, 15 layers. Maximum y⁺ at Re_D = 1×10⁵: 1.25–1.6 on the pipe wall and 3.3–3.9 on the plate, inside the viscous sublayer (y⁺ < 5).
- **Mesh independence:** four meshes refined with a ratio of about 1.3, discretization uncertainty with the Grid Convergence Index (Celik et al., 2008).
- **Cd from CFD:** flow rate imposed at the inlet, ΔP read at the flange tap locations, Cd = V·√(1−β⁴) / (β²·√(2ΔP/ρ)).
- **Reference:** RHG equation, implemented in [`postprocessing/rhg_cd.py`](postprocessing/rhg_cd.py) and cross-checked against the open-source [`fluids`](https://fluids.readthedocs.io) library.

Reference values for this case:

| Re_D | Inlet velocity [m/s] | Cd (RHG) |
|---:|---:|---:|
| 5×10⁴ | 0.4906 | 0.61377 |
| 1×10⁵ | 0.9812 | 0.61082 |
| 3×10⁵ | 2.9437 | 0.60787 |
| 5×10⁵ | 4.9062 | 0.60693 |

## Results so far

### Mesh independence (Re_D = 1×10⁵, k-ω SST)

The only differences between meshes are the global element size and the edge sizing on the plate and on the pipe wall between the taps. The inflation is the same in all of them.

| Mesh | Global / edge size [mm] | Cells | Min. orthogonal quality | Cd (CFD) | Error vs RHG |
|---|---|---:|---:|---:|---:|
| R01 Coarse | 2.75 / 1.40 | 37 948 | 0.154 | 0.63734 | +4.34 % |
| R02 Medium | 2.00 / 1.00 | 62 696 | 0.193 | 0.61820 | +1.21 % |
| R03 Fine | 1.45 / 0.72 | 104 613 | 0.221 | 0.61940 | +1.40 % |
| R08 Extra fine | 1.08 / 0.56 | 181 916 | 0.305 | 0.61696 | +1.01 % |

GCI with the medium, fine and extra-fine meshes (refinement ratios 1.29 and 1.32):

| Quantity | Value |
|---|---|
| Convergence type | Oscillatory (±0.2 %) |
| Apparent order p | 2.44 (formal order of the scheme: 2) |
| Extrapolated Cd | 0.61443 (+0.59 % vs RHG) |
| **GCI, extra-fine mesh** | **0.51 %** |
| Check: half the oscillation range (Stern et al., 2001) | 0.20 % |
| Conservative bound: p = 2, Fs = 3 (Roache, 1998) | 1.6 % |

The coarse mesh is left out of the GCI. Its edge sizing (1.4 mm) resolves the 1.5 mm orifice bore edge, where the flow separates, with a single cell. With it, the apparent order comes out at about 11, which is not physical. From the medium mesh on, the Cd stays within ±0.2 %.

**Reading:** the discretization uncertainty (about 0.5 %) is smaller than the 1.0–1.4 % difference from ISO 5167-2. That difference therefore comes mainly from the model (turbulence model and uniform inlet profile), not from the mesh. The uncertainty of the RHG equation itself is ±0.5 % for β = 0.6.

### Transient start-up (R09)

The pipe starts full of still water. At the inlet, the velocity ramps linearly from 0 to the Re_D = 1×10⁵ value in 0.1 s. The run uses the medium mesh, URANS k-ω SST, bounded second-order implicit time stepping and Δt = 1 ms. It ran up to t = 0.794 s.

- A starting vortex ring rolls up at the orifice edge and travels downstream, followed by the jet shear layer and the build-up of the recirculation zone.
- During the ramp, the tap pressures are dominated by the acceleration of the water column. The ~20 kPa seen at P1 matches ρ·a·L for the pipe length downstream of the tap.
- After the ramp, the Cd settles to **0.61688** at t = 0.794 s, within 0.2 % of the steady-state value on the same mesh (0.61820).

The start-up run is used for visualization. It is not part of the Cd validation.

## Repository structure

```
geometry/         Dimensioned drawing and CAD export of the fluid domain
mesh/             Mesh settings and statistics
setup/            Fluent settings and journals
results/raw/      Raw exported data (tap pressures, wall pressure, profiles)
postprocessing/   Python scripts: reference Cd, CFD Cd, GCI, figures
report/           Technical report
```

## Roadmap

- [x] Phase 0 — Setup: repository, simulation log, reference correlation
- [x] Phase 1 — Geometry and mesh, mesh independence study (GCI)
- [x] Transient start-up run and flow animations
- [ ] Phase 2 — Simulations at four Reynolds numbers and Cd validation (thinner first layer at Re_D = 3×10⁵ and 5×10⁵ to keep y⁺ < 5)
- [ ] Phase 3 — Report and results summary
- [ ] Phase 4 — Possible extension: upstream elbow installation effects

## Hardware

Intel Core i5-8265U (4 cores, 8 threads), 20 GB RAM. ANSYS Fluent runs on the CPU.

## References

- ISO 5167-2:2003, *Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full — Part 2: Orifice plates*. The discharge coefficient equation is unchanged in ISO 5167-2:2022. The standard is copyrighted and is not distributed in this repository.
- M. J. Reader-Harris, *Orifice Plates and Venturi Tubes*, Springer, 2015.
- I. B. Celik et al., *Procedure for Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications*, Journal of Fluids Engineering 130(7), 2008.
- F. Stern, R. V. Wilson, H. W. Coleman, E. G. Paterson, *Comprehensive Approach to Verification and Validation of CFD Simulations—Part 1: Methodology and Procedures*, Journal of Fluids Engineering 123(4), 2001.
- P. J. Roache, *Verification and Validation in Computational Science and Engineering*, Hermosa Publishers, 1998.
- S. Benhamadouche, W. J. Malouf, M. Arenas, *Effects of Spatial Discretisation and RANS Turbulence Modelling on the Numerical Simulation of a Flow Through a Square-Edged Orifice in a Round Pipe*, 36th IAHR World Congress, 2015.

## Author

Luis Arango — Mechanical Engineer.
