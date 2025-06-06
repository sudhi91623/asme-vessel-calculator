import pandas as pd

def get_material_properties(material, temperature):
    """
    Lookup allowable stress from materials.csv for a given material and temperature.
    """
    try:
        df = pd.read_csv("data/materials.csv")
        row = df[(df["Material"] == material) & (df["Temp_C"] == int(temperature))]
        if not row.empty:
            return float(row["Allowable_Stress_MPa"].values[0])
    except Exception as e:
        print(f"Error reading material properties: {e}")
    return None

def get_chart_allowable_pressure(curve, D_o, L):
    """
    Returns a rough estimate of allowable pressure from UG-28 based on curve selection and L/D.
    This is a simplified version using assumed curve behavior.
    """
    ratio = L / D_o
    if curve == "Curve B":
        if ratio <= 2: return 0.40
        elif ratio <= 4: return 0.30
        else: return 0.20
    elif curve == "Curve D":
        if ratio <= 2: return 0.60
        elif ratio <= 4: return 0.45
        else: return 0.35
    return 0.0
