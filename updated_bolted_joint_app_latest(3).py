
import streamlit as st

# Define tensile stress areas for UNC fasteners
tensile_stress_areas = {
    '1/2-13': 0.1419,
    '5/8-11': 0.226,
    '3/4-10': 0.334,
    '7/8-9': 0.462,
    '1-8': 0.606,
    '1 1/8-8': 0.763
}

# Define material tensile strengths in ksi
material_strengths = {
    'A193 B7': 125,
    'A193 B7M': 105,
    'A193 B8': 125,
    'A193 B8M': 105,
    'A307 Gr. B': 60,
    'A574': 170
}

# Define diameter mapping for UNC fasteners
diameter_mapping = {
    '1/2': 0.5,
    '5/8': 0.625,
    '3/4': 0.75,
    '7/8': 0.875,
    '1': 1.0,
    '1 1/8': 1.125
}

# Function to calculate preload
def calculate_preload(torque, diameter, k_factor):
    return (torque * 12) / (k_factor * diameter)

# Function to calculate clamping force
def calculate_clamping_force(preload, quantity):
    return preload * quantity

# Function to calculate equivalent strength in ksi
def calculate_equivalent_strength(clamping_force, tensile_stress_area):
    return (clamping_force / tensile_stress_area) / 1000

# Function to extract TPI from UNC fastener size
def extract_tpi(fastener_size):
    return int(fastener_size.split('-')[1])

# Streamlit app
st.title("Bolted Joint Analysis")

# Input fields for Joint 1
st.header("Joint 1")
fastener_size_1 = st.selectbox("Fastener Size (UNC)", list(tensile_stress_areas.keys()), key="fastener_size_1")
quantity_1 = st.number_input("Number of Fasteners", min_value=1, key="quantity_1")
material_1 = st.selectbox("Fastener Grade", list(material_strengths.keys()), key="material_1")
torque_1 = st.number_input("Torque (ft-lb)", min_value=0.0, key="torque_1")
k_factor_1 = st.number_input("k-factor (friction factor)", min_value=0.0, value=0.17, key="k_factor_1")

# Input fields for Joint 2
st.header("Joint 2")
fastener_size_2 = st.selectbox("Fastener Size (UNC)", list(tensile_stress_areas.keys()), key="fastener_size_2")
quantity_2 = st.number_input("Number of Fasteners", min_value=1, key="quantity_2")
material_2 = st.selectbox("Fastener Grade", list(material_strengths.keys()), key="material_2")
torque_2 = st.number_input("Torque (ft-lb)", min_value=0.0, key="torque_2")
k_factor_2 = st.number_input("k-factor (friction factor)", min_value=0.0, value=0.17, key="k_factor_2")

# Calculate values for Joint 1
diameter_1 = diameter_mapping[fastener_size_1.split('-')[0]]
tpi_1 = extract_tpi(fastener_size_1)
preload_1 = calculate_preload(torque_1, diameter_1, k_factor_1)
clamping_force_1 = calculate_clamping_force(preload_1, quantity_1)
equivalent_strength_1 = calculate_equivalent_strength(clamping_force_1, tensile_stress_areas[fastener_size_1])

# Calculate values for Joint 2
diameter_2 = diameter_mapping[fastener_size_2.split('-')[0]]
tpi_2 = extract_tpi(fastener_size_2)
preload_2 = calculate_preload(torque_2, diameter_2, k_factor_2)
clamping_force_2 = calculate_clamping_force(preload_2, quantity_2)
equivalent_strength_2 = calculate_equivalent_strength(clamping_force_2, tensile_stress_areas[fastener_size_2])

# Calculate strength ratio
strength_ratio = (equivalent_strength_2 / equivalent_strength_1) * 100 if equivalent_strength_1 != 0 else 0

# Determine result
result = "PASS" if strength_ratio <= 60 else "FAIL"

# Display results
st.subheader("Results")
st.write(f"Preload for Joint 1: {preload_1:.2f} lbf")
st.write(f"Clamping Force for Joint 1: {clamping_force_1:.2f} lbf")
st.write(f"Equivalent Strength for Joint 1: {equivalent_strength_1:.2f} ksi")
st.write(f"Preload for Joint 2: {preload_2:.2f} lbf")
st.write(f"Clamping Force for Joint 2: {clamping_force_2:.2f} lbf")
st.write(f"Equivalent Strength for Joint 2: {equivalent_strength_2:.2f} ksi")
st.write(f"Strength Ratio: {strength_ratio:.2f}%")
st.write(f"Result: {result}")

# Display formulas used
st.subheader("Formulas Used")
st.latex(r"	ext{Preload} = rac{	ext{Torque} 	imes 12}{k 	imes 	ext{Diameter}}")
st.latex(r"	ext{Clamping Force} = 	ext{Preload} 	imes 	ext{Quantity}")
st.latex(r"	ext{Equivalent Strength} = rac{	ext{Clamping Force}}{	ext{Tensile Stress Area}} \div 1000")
st.latex(r"	ext{Strength Ratio} = \left( rac{	ext{Joint 2 Strength}}{	ext{Joint 1 Strength}} ight) 	imes 100")
