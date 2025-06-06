def calculate_shell_thickness(P, R, S, E, CA):
    """
    UG-27(c)(1): Internal pressure thickness calculation for cylindrical shells.
    
    P = Internal Pressure (MPa)
    R = Internal Radius (mm)
    S = Allowable Stress (MPa)
    E = Weld Joint Efficiency
    CA = Corrosion Allowance (mm)
    """
    t_required = (P * R) / (S * E - 0.6 * P)
    t_nominal = t_required + CA
    return t_required, t_nominal
