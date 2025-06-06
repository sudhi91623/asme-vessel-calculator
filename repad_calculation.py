def calculate_repad_area(d_nozzle, t_shell, t_nozzle, t_repad, d_repad):
    """
    Calculate required and available reinforcement area for a nozzle.

    d_nozzle: Nozzle diameter (mm)
    t_shell: Shell thickness (mm)
    t_nozzle: Nozzle thickness (mm)
    t_repad: Repad thickness (mm)
    d_repad: Repad outer diameter (mm)
    """
    A_required = d_nozzle * t_shell

    A_from_nozzle = d_nozzle * t_nozzle
    A_from_repad = 3.1416 * ((d_repad / 2)**2 - (d_nozzle / 2)**2) * (t_repad / d_nozzle)

    A_total = A_from_nozzle + A_from_repad

    return A_required, A_total
