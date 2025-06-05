
# Import necessary libraries
import streamlit as st

# Define tensile stress areas for UNC fasteners
tensile_stress_areas = {
    "1/2-13": 0.1419,
    "5/8-11": 0.226,
    "3/4-10": 0.334,
    "7/8-9": 0.462,
    "1-8": 0.606,
    "1 1/8-8": 0.763
}

# Define material strengths in psi
material_strengths = {
    "ASTM A193": 125000,
    "ASTM A320": 105000,
    "ASTM A307": 60000,
    "ASTM A574": 170000
}

# Function to calculate preload
def calculate_preload(torque, k_factor, diameter):
    return (torque * 12) / (k_factor * diameter)

# Function to calculate clamping force
def calculate_clamping_force(preload, quantity):
    return preload * quantity

# Function to calculate equivalent strength in ksi
def calculate_equivalent_strength(clamping_force, tensile_stress_area):
    return (clamping_force / tensile_stress_area) / 1000

# Streamlit app
st.title("Bolted Joint Analysis App")

# Input fields for Joint 1
st.header("Joint 1")
diameter_1 = st.selectbox("Fastener Diameter (UNC standard)", list(tensile_stress_areas.keys()), key="diameter_1")
tpi_1 = st.text_input("Threads per Inch (TPI)", key="tpi_1")
quantity_1 = st.number_input("Number of Fasteners", min_value=1, key="quantity_1")
grade_1 = st.selectbox("Fastener Grade", list(material_strengths.keys()), key="grade_1")
torque_1 = st.number_input("Torque (ft-lb)", min_value=0.0, key="torque_1")
k_factor_1 = st.number_input("k-factor (friction factor)", min_value=0.0, value=0.17, key="k_factor_1")

# Input fields for Joint 2
st.header("Joint 2")
diameter_2 = st.selectbox("Fastener Diameter (UNC standard)", list(tensile_stress_areas.keys()), key="diameter_2")
tpi_2 = st.text_input("Threads per Inch (TPI)", key="tpi_2")
quantity_2 = st.number_input("Number of Fasteners", min_value=1, key="quantity_2")
grade_2 = st.selectbox("Fastener Grade", list(material_strengths.keys()), key="grade_2")
torque_2 = st.number_input("Torque (ft-lb)", min_value=0.0, key="torque_2")
k_factor_2 = st.number_input("k-factor (friction factor)", min_value=0.0, value=0.17, key="k_factor_2")

# Calculate values for Joint 1
preload_1 = calculate_preload(torque_1, k_factor_1, tensile_stress_areas[diameter_1])
clamping_force_1 = calculate_clamping_force(preload_1, quantity_1)
equivalent_strength_1 = calculate_equivalent_strength(clamping_force_1, tensile_stress_areas[diameter_1])

# Calculate values for Joint 2
preload_2 = calculate_preload(torque_2, k_factor_2, tensile_stress_areas[diameter_2])
clamping_force_2 = calculate_clamping_force(preload_2, quantity_2)
equivalent_strength_2 = calculate_equivalent_strength(clamping_force_2, tensile_stress_areas[diameter_2])

# Calculate strength ratio
if equivalent_strength_1 != 0:
    strength_ratio = (equivalent_strength_2 / equivalent_strength_1) * 100
else:
    strength_ratio = 0

# Determine pass/fail result
result = "PASS" if strength_ratio <= 60 else "FAIL"

# Display results
st.header("Results")
st.write(f"Preload for Joint 1: {preload_1:.2f} lbf")
st.write(f"Clamping Force for Joint 1: {clamping_force_1:.2f} lbf")
st.write(f"Equivalent Strength for Joint 1: {equivalent_strength_1:.2f} ksi")
st.write(f"Preload for Joint 2: {preload_2:.2f} lbf")
st.write(f"Clamping Force for Joint 2: {clamping_force_2:.2f} lbf")
st.write(f"Equivalent Strength for Joint 2: {equivalent_strength_2:.2f} ksi")
st.write(f"Strength Ratio: {strength_ratio:.2f}%")
st.write(f"Result: {result}")

# Display summary of formulas used
st.header("Summary of Formulas Used")
st.latex(r"\text{Preload} = \frac{\text{Torque} \times 12}{k \times \text{Diameter}}")
st.latex(r"\text{Clamping Force} = \text{Preload} \times \text{Quantity}")
st.latex(r"\text{Equivalent Strength (ksi)} = \frac{\text{Clamping Force (lbf)}}{\text{Tensile Stress Area (in}^2)} \div 1000")
st.latex(r"\text{Strength Ratio} = \left( \frac{\text{Joint 2 Strength}}{\text{Joint 1 Strength}} \right) \times 100")
