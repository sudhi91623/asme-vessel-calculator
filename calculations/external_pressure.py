def calculate_external_pressure_thickness(P_ext, D_o, L):
    """
    UG-28: Estimate required thickness for external pressure.
    
    P_ext = External Pressure (MPa)
    D_o = Outside Diameter (mm)
    L = Unsupported Length (mm)
    """
    # Conservative empirical constant (for demo purpose)
    F = 0.25
    t = (P_ext * D_o) / F
    return t
