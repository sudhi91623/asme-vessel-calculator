# app.py (Streamlit entry point)
import streamlit as st
from calculations.shell_thickness import calculate_shell_thickness
from calculations.head_thickness import calculate_ellipsoidal_head_thickness
from calculations.external_pressure import calculate_external_pressure_thickness
from calculations.repad_calculation import calculate_repad_area
from calculations.hydrotest import calculate_hydrotest_pressure
from calculations.utils import get_material_properties, get_chart_allowable_pressure
from fpdf import FPDF
import os

st.set_page_config(page_title="ASME Sec VIII Div 1 Calculator", layout="centered")
st.title("ASME Sec VIII Div.1 (2023) Pressure Vessel Calculator")

results = []

# UG-27 Shell
st.header("Cylindrical Shell Thickness (UG-27)")
with st.form("ug27_form"):
    P = st.number_input("Design Pressure (MPa)", min_value=0.01, value=1.0, step=0.1)
    R = st.number_input("Inside Radius (mm)", min_value=10.0, value=500.0, step=10.0)
    mat = st.selectbox("Material", options=["SA-516-70", "SA-240-304", "SA-105"])
    temp = st.number_input("Design Temperature (°C)", min_value=20.0, value=100.0, step=10.0)
    E = st.slider("Weld Joint Efficiency (E)", 0.7, 1.0, value=0.85)
    CA = st.number_input("Corrosion Allowance (mm)", min_value=0.0, value=1.0)
    submitted = st.form_submit_button("Calculate Shell Thickness")

if submitted:
    S = get_material_properties(mat, temp)
    if S:
        t_required, t_nominal = calculate_shell_thickness(P, R, S, E, CA)
        result = f"UG-27 Shell Thickness: Required = {t_required:.2f} mm, Nominal = {t_nominal:.2f} mm"
        st.success(result)
        results.append(result)
    else:
        st.error("Material properties not found for selected temperature.")

# UG-32 Head
st.header("Ellipsoidal Head Thickness (UG-32)")
with st.form("ug32_elliptical"):
    P_h = st.number_input("Design Pressure (MPa) - Head", min_value=0.01, value=1.0, step=0.1)
    D = st.number_input("Head Inside Diameter (mm)", min_value=100.0, value=1000.0, step=10.0)
    mat_h = st.selectbox("Material (Head)", options=["SA-516-70", "SA-240-304", "SA-105"], key="head_mat")
    temp_h = st.number_input("Design Temperature (°C) - Head", min_value=20.0, value=100.0, step=10.0, key="head_temp")
    E_h = st.slider("Weld Joint Efficiency (E) - Head", 0.7, 1.0, value=0.85, key="head_E")
    CA_h = st.number_input("Corrosion Allowance (mm) - Head", min_value=0.0, value=1.0, key="head_CA")
    submitted_h = st.form_submit_button("Calculate Head Thickness")

if submitted_h:
    S_h = get_material_properties(mat_h, temp_h)
    if S_h:
        t_head_required, t_head_nominal = calculate_ellipsoidal_head_thickness(P_h, D, S_h, E_h, CA_h)
        result = f"UG-32 Head Thickness: Required = {t_head_required:.2f} mm, Nominal = {t_head_nominal:.2f} mm"
        st.success(result)
        results.append(result)
    else:
        st.error("Material properties not found for selected temperature.")

# UG-28 External Pressure
st.header("External Pressure Thickness (UG-28)")
with st.form("ug28_external"):
    P_ext = st.number_input("External Pressure (MPa)", min_value=0.01, value=0.1, step=0.01)
    D_o = st.number_input("Outside Diameter (mm)", min_value=100.0, value=1000.0, step=10.0)
    L = st.number_input("Unsupported Length (mm)", min_value=100.0, value=2000.0, step=10.0)
    curve = st.selectbox("Material Curve (UG-28 Chart)", options=["Curve B", "Curve D"])
    submitted_ext = st.form_submit_button("Calculate External Thickness")

if submitted_ext:
    allowable = get_chart_allowable_pressure(curve, D_o, L)
    t_ext = calculate_external_pressure_thickness(P_ext, D_o, L)
    result = f"UG-28 External Pressure: Thickness = {t_ext:.2f} mm, Allowable Pressure ({curve}) = {allowable:.3f} MPa"
    st.success(result)
    results.append(result)

# Appendix 1-7: Reinforcement Pad
st.header("Nozzle Reinforcement Area (Appendix 1-7)")
with st.form("repad_form"):
    d_nozzle = st.number_input("Nozzle Diameter (mm)", min_value=10.0, value=100.0, step=5.0)
    t_shell = st.number_input("Shell Thickness (mm)", min_value=5.0, value=12.0, step=1.0)
    t_nozzle = st.number_input("Nozzle Thickness (mm)", min_value=5.0, value=10.0, step=1.0)
    t_repad = st.number_input("Repad Thickness (mm)", min_value=5.0, value=8.0, step=1.0)
    d_repad = st.number_input("Repad Outer Diameter (mm)", min_value=100.0, value=200.0, step=5.0)
    submitted_rp = st.form_submit_button("Calculate Reinforcement Area")

if submitted_rp:
    required_area, available_area = calculate_repad_area(d_nozzle, t_shell, t_nozzle, t_repad, d_repad)
    result = f"Appendix 1-7 Reinforcement: Required = {required_area:.2f} mm², Available = {available_area:.2f} mm²"
    st.success(result)
    results.append(result)

# UG-99 Hydrotest Pressure
st.header("Hydrotest Pressure (UG-99)")
with st.form("hydrotest_form"):
    MAWP = st.number_input("Maximum Allowable Working Pressure (MAWP) (MPa)", min_value=0.1, value=1.5, step=0.1)
    factor = st.slider("Test Pressure Factor (typical 1.3x to 1.5x)", min_value=1.0, max_value=2.0, value=1.3)
    submitted_ht = st.form_submit_button("Calculate Hydrotest Pressure")

if submitted_ht:
    test_pressure = calculate_hydrotest_pressure(MAWP, factor)
    result = f"UG-99 Hydrotest Pressure: {test_pressure:.2f} MPa"
    st.success(result)
    results.append(result)

# PDF Report Generation
st.header("📄 Generate PDF Report")
project = st.text_input("Enter Project Name", value="My_Vessel_Project")
if st.button("Download PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"ASME Sec VIII Div 1 Report - {project}", ln=True, align='C')
    pdf.ln(10)
    for line in results:
        pdf.multi_cell(0, 10, txt=line)
    pdf.output("report.pdf")
    with open("report.pdf", "rb") as f:
        st.download_button(label="📥 Download Report", data=f, file_name=f"{project}_ASME_Report.pdf")
    os.remove("report.pdf")
