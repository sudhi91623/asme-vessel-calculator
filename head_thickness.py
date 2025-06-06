def calculate_ellipsoidal_head_thickness(P, D, S, E, CA):
    """
    UG-32: Thickness for 2:1 Ellipsoidal Heads

    P = Internal Pressure (MPa)
    D = Inside Diameter (mm)
    S = Allowable Stress (MPa)
    E = Weld Joint Efficiency
    CA = Corrosion Allowance (mm)
    """
    K = 0.90  # Form factor for ellipsoidal heads (per UG-32(c))
    t_required = (P * D) / (2 * K * S * E - 0.2 * P)
    t_nominal = t_required + CA
    return t_required, t_nominal
