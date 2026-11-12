"""Reference discharge coefficient for the orifice plate case.

Computes the Reader-Harris/Gallagher (1998) discharge coefficient of
ISO 5167-2:2003 (Eq. 4) for flange tappings, plus the inlet velocity to
impose in Fluent for each target pipe Reynolds number, and a helper to
compute Cd from a CFD result (imposed flow rate + measured dP).

Usage:
    python rhg_cd.py
"""
import math

# --- Case parameters (see geometry/Plano_dominio_placa_orificio.pdf) ---
D_MM = 102.3          # pipe internal diameter [mm] (4" Sch 40)
BETA = 0.6            # diameter ratio d/D [-]
RHO = 998.2           # water at 20 C [kg/m3]
MU = 1.002e-3         # water at 20 C [Pa s]
RE_TARGETS = (5e4, 1e5, 3e5, 5e5)


def cd_rhg(beta: float, re_d: float, d_mm: float, taps: str = "flange") -> float:
    """Reader-Harris/Gallagher discharge coefficient (ISO 5167-2:2003, Eq. 4)."""
    if taps == "flange":
        l1 = l2 = 25.4 / d_mm
    elif taps == "corner":
        l1 = l2 = 0.0
    elif taps == "D-D/2":
        l1, l2 = 1.0, 0.47
    else:
        raise ValueError("taps must be 'flange', 'corner' or 'D-D/2'")

    a = (19000.0 * beta / re_d) ** 0.8
    m2 = 2.0 * l2 / (1.0 - beta)
    c = (0.5961 + 0.0261 * beta**2 - 0.216 * beta**8
         + 0.000521 * (1e6 * beta / re_d) ** 0.7
         + (0.0188 + 0.0063 * a) * beta**3.5 * (1e6 / re_d) ** 0.3
         + (0.043 + 0.080 * math.exp(-10 * l1) - 0.123 * math.exp(-7 * l1))
         * (1 - 0.11 * a) * beta**4 / (1 - beta**4)
         - 0.031 * (m2 - 0.8 * m2**1.1) * beta**1.3)
    if d_mm < 71.12:  # small-pipe term
        c += 0.011 * (0.75 - beta) * (2.8 - d_mm / 25.4)
    return c


def inlet_velocity(re_d: float, d_mm: float = D_MM, rho: float = RHO, mu: float = MU) -> float:
    """Mean inlet velocity [m/s] that gives the target pipe Reynolds number."""
    return re_d * mu / (rho * d_mm / 1000.0)


def cd_from_cfd(v_inlet: float, dp: float, beta: float = BETA, rho: float = RHO) -> float:
    """Cd from CFD: imposed mean pipe velocity [m/s] and dP = P1 - P2 [Pa] (epsilon = 1)."""
    return v_inlet * math.sqrt(1 - beta**4) / (beta**2 * math.sqrt(2 * dp / rho))


def check_limits(beta: float, re_d: float, d_mm: float) -> bool:
    """ISO 5167-2:2003 limits of use for flange tappings."""
    return (50 <= d_mm <= 1000 and 0.1 <= beta <= 0.75
            and re_d >= 5000 and re_d >= 170 * beta**2 * d_mm)


if __name__ == "__main__":
    print(f"D = {D_MM} mm, beta = {BETA}, d = {BETA * D_MM:.2f} mm, water at 20 C\n")
    print(f"{'Re_D':>10} {'V_inlet [m/s]':>14} {'Cd (RHG)':>10} {'ISO limits':>11}")
    for re in RE_TARGETS:
        print(f"{re:>10.0e} {inlet_velocity(re):>14.4f} {cd_rhg(BETA, re, D_MM):>10.5f} "
              f"{'OK' if check_limits(BETA, re, D_MM) else 'OUT':>11}")
