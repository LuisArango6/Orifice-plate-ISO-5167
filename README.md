# Orifice-plate-ISO-5167

CFD validation of an orifice plate discharge coefficient (Cd) against ISO 5167-2 (Reader-Harris/Gallagher) for an oil & gas water-injection metering case. 2D axisymmetric RANS in ANSYS Fluent, mesh independence study with GCI, 4" line, β = 0.6, flange taps, Re 5×10⁴–5×10⁵.

> **Status:** 🚧 Work in progress — Phase 1 (geometry and mesh).

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
- **Solver:** ANSYS Fluent 2026 R1 (Student), pressure-based, steady state.
- **Turbulence:** k-ω SST (baseline), with a second model for sensitivity.
- **Near-wall resolution:** y⁺ ≈ 1 with inflation layers.
- **Mesh independence:** three systematically refined meshes, discretization uncertainty with the Grid Convergence Index (Celik et al., 2008).
- **Cd from CFD:** flow rate imposed at the inlet, ΔP read at the flange tap locations, Cd = V·√(1−β⁴) / (β²·√(2ΔP/ρ)).
- **Reference:** RHG equation, implemented in [`postprocessing/rhg_cd.py`](postprocessing/rhg_cd.py) and cross-checked against the open-source [`fluids`](https://fluids.readthedocs.io) library.

Reference values for this case:

| Re_D | Inlet velocity [m/s] | Cd (RHG) |
|---:|---:|---:|
| 5×10⁴ | 0.4906 | 0.61377 |
| 1×10⁵ | 0.9812 | 0.61082 |
| 3×10⁵ | 2.9437 | 0.60787 |
| 5×10⁵ | 4.9062 | 0.60693 |

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
- [ ] Phase 1 — Geometry and mesh, mesh independence study (GCI)
- [ ] Phase 2 — Simulations at four Reynolds numbers and Cd validation
- [ ] Phase 3 — Report and results summary
- [ ] Phase 4 — Possible extension: upstream elbow installation effects

## Hardware

Intel Core i5-8265U (4 cores, 8 threads), 20 GB RAM. ANSYS Fluent runs on the CPU.

## References

- ISO 5167-2:2003, *Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full — Part 2: Orifice plates*. The discharge coefficient equation is unchanged in ISO 5167-2:2022. The standard is copyrighted and is not distributed in this repository.
- M. J. Reader-Harris, *Orifice Plates and Venturi Tubes*, Springer, 2015.
- I. B. Celik et al., *Procedure for Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications*, Journal of Fluids Engineering 130(7), 2008.
- S. Benhamadouche, W. J. Malouf, M. Arenas, *Effects of Spatial Discretisation and RANS Turbulence Modelling on the Numerical Simulation of a Flow Through a Square-Edged Orifice in a Round Pipe*, 36th IAHR World Congress, 2015.

## Author

Luis Arango — Mechanical Engineer.
