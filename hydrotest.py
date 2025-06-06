def calculate_hydrotest_pressure(MAWP, factor):
    """
    UG-99: Hydrostatic test pressure calculation.

    MAWP = Maximum Allowable Working Pressure (MPa)
    factor = Test pressure factor (typically 1.3x to 1.5x)
    """
    return MAWP * factor
