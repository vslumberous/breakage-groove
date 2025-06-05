
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

# Define material strengths for fastener grades
fastener_grades = {
    "ASTM A193 B7": 125000,   # psi
    "ASTM A193 B7M": 100000,  # psi
    "ASTM A193 B8": 75000,    # psi
    "ASTM A193 B8M": 75000,   # psi
    "ASTM A320": 105000,      # psi
    "ASTM A307 Gr. B": 60000, # psi
    "ASTM A574": 170000       # psi
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

# Function to calculate strength ratio
def calculate_strength_ratio(strength_1, strength_2):
    return (strength_2 / strength_1) * 100

# Streamlit app
st.title("Bolted Joint Analysis")

# Input fields for Joint 1
st.header("Joint 1")
diameter_1 = st.selectbox("Fastener Diameter (UNC standard)", list(tensile_stress_areas.keys()), key="joint1_diameter")
num_fasteners_1 = st.number_input("Number of Fasteners", min_value=1, step=1, key="joint1_num_fasteners")
grade_1 = st.selectbox("Fastener Grade", list(fastener_grades.keys()), key="joint1_grade")
torque_1 = st.number_input("Torque (ft-lb)", min_value=0.0, step=0.1, key="joint1_torque")
k_factor_1 = st.number_input("k-factor (friction factor)", value=0.17, step=0.01, key="joint1_k_factor")

# Input fields for Joint 2
st.header("Joint 2")
diameter_2 = st.selectbox("Fastener Diameter (UNC standard)", list(tensile_stress_areas.keys()), key="joint2_diameter")
num_fasteners_2 = st.number_input("Number of Fasteners", min_value=1, step=1, key="joint2_num_fasteners")
grade_2 = st.selectbox("Fastener Grade", list(fastener_grades.keys()), key="joint2_grade")
torque_2 = st.number_input("Torque (ft-lb)", min_value=0.0, step=0.1, key="joint2_torque")
k_factor_2 = st.number_input("k-factor (friction factor)", value=0.17, step=0.01, key="joint2_k_factor")

if st.button("Calculate"):
    # Calculate values for Joint 1
    preload_1 = calculate_preload(torque_1, k_factor_1, tensile_stress_areas[diameter_1])
    clamping_force_1 = calculate_clamping_force(preload_1, num_fasteners_1)
    equivalent_strength_1 = calculate_equivalent_strength(clamping_force_1, tensile_stress_areas[diameter_1])
    material_strength_1 = fastener_grades[grade_1]

    # Calculate values for Joint 2
    preload_2 = calculate_preload(torque_2, k_factor_2, tensile_stress_areas[diameter_2])
    clamping_force_2 = calculate_clamping_force(preload_2, num_fasteners_2)
    equivalent_strength_2 = calculate_equivalent_strength(clamping_force_2, tensile_stress_areas[diameter_2])
    material_strength_2 = fastener_grades[grade_2]

    # Calculate strength ratio
    strength_ratio = calculate_strength_ratio(equivalent_strength_1, equivalent_strength_2)
    result = "PASS" if strength_ratio <= 60 else "FAIL"

    # Display results
    st.subheader("Results")
    st.write(f"**Joint 1**")
    st.write(f"Preload: {preload_1:.2f} lbf")
    st.write(f"Clamping Force: {clamping_force_1:.2f} lbf")
    st.write(f"Equivalent Strength: {equivalent_strength_1:.2f} ksi")
    st.write(f"Material Strength: {material_strength_1} psi")

    st.write(f"**Joint 2**")
    st.write(f"Preload: {preload_2:.2f} lbf")
    st.write(f"Clamping Force: {clamping_force_2:.2f} lbf")
    st.write(f"Equivalent Strength: {equivalent_strength_2:.2f} ksi")
    st.write(f"Material Strength: {material_strength_2} psi")

    st.write(f"**Strength Ratio: {strength_ratio:.2f}%**")
    st.write(f"**Result: {result}**")

    # Display formulas used
    st.subheader("Formulas Used")
    st.latex(r"	ext{Preload} = rac{	ext{Torque} 	imes 12}{k 	imes 	ext{Diameter}}")
    st.latex(r"	ext{Clamping Force} = 	ext{Preload} 	imes 	ext{Quantity}")
    st.latex(r"	ext{Equivalent Strength} = rac{	ext{Clamping Force}}{	ext{Tensile Stress Area}} \div 1000")
    st.latex(r"	ext{Strength Ratio} = \left( rac{	ext{Joint 2 Strength}}{	ext{Joint 1 Strength}} ight) 	imes 100")

    # Display step-by-step calculations
    st.subheader("Step-by-Step Calculations")
    st.write(f"**Joint 1 Calculations**")
    st.write(f"Preload = ({torque_1} ft-lb * 12) / ({k_factor_1} * {tensile_stress_areas[diameter_1]}) = {preload_1:.2f} lbf")
    st.write(f"Clamping Force = {preload_1:.2f} lbf * {num_fasteners_1} = {clamping_force_1:.2f} lbf")
    st.write(f"Equivalent Strength = {clamping_force_1:.2f} lbf / {tensile_stress_areas[diameter_1]} in² / 1000 = {equivalent_strength_1:.2f} ksi")

    st.write(f"**Joint 2 Calculations**")
    st.write(f"Preload = ({torque_2} ft-lb * 12) / ({k_factor_2} * {tensile_stress_areas[diameter_2]}) = {preload_2:.2f} lbf")
    st.write(f"Clamping Force = {preload_2:.2f} lbf * {num_fasteners_2} = {clamping_force_2:.2f} lbf")
    st.write(f"Equivalent Strength = {clamping_force_2:.2f} lbf / {tensile_stress_areas[diameter_2]} in² / 1000 = {equivalent_strength_2:.2f} ksi")

    st.write(f"**Strength Ratio Calculation**")
    st.write(f"Strength Ratio = ({equivalent_strength_2:.2f} ksi / {equivalent_strength_1:.2f} ksi) * 100 = {strength_ratio:.2f}%")
