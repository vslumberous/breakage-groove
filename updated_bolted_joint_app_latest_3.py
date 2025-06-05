
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

# Define fastener grades and their properties
fastener_grades = {
    "ASTM A193 B7": {"UTS": 125000, "YS": 105000},
    "ASTM A193 B7M": {"UTS": 100000, "YS": 75000},
    "ASTM A193 B8": {"UTS": 75000, "YS": 30000},
    "ASTM A193 B8M": {"UTS": 75000, "YS": 30000},
    "ASTM A320": {"UTS": 105000, "YS": 75000},
    "ASTM A307 Gr. B": {"UTS": 60000, "YS": 36000},
    "ASTM A574": {"UTS": 170000, "YS": 140000}
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

# Streamlit app
st.title("Bolted Joint Analysis App")

st.header("Joint 1")
diameter1 = st.selectbox("Fastener Diameter (UNC)", list(tensile_stress_areas.keys()), key="joint1_diameter")
num_fasteners1 = st.number_input("Number of Fasteners", value=1, step=1, key="joint1_num_fasteners")
grade1 = st.selectbox("Fastener Grade", list(fastener_grades.keys()), key="joint1_grade")
torque1 = st.number_input("Torque (ft-lb)", value=10.0, step=0.1, key="joint1_torque")
k_factor1 = st.number_input("k-factor (friction factor)", value=0.17, step=0.01, key="joint1_k_factor")

st.header("Joint 2")
diameter2 = st.selectbox("Fastener Diameter (UNC)", list(tensile_stress_areas.keys()), key="joint2_diameter")
num_fasteners2 = st.number_input("Number of Fasteners", value=1, step=1, key="joint2_num_fasteners")
grade2 = st.selectbox("Fastener Grade", list(fastener_grades.keys()), key="joint2_grade")
torque2 = st.number_input("Torque (ft-lb)", value=10.0, step=0.1, key="joint2_torque")
k_factor2 = st.number_input("k-factor (friction factor)", value=0.17, step=0.01, key="joint2_k_factor")

if st.button("Calculate"):
    # Calculate preload for both joints
    preload1 = calculate_preload(torque1, tensile_stress_areas[diameter1], k_factor1)
    preload2 = calculate_preload(torque2, tensile_stress_areas[diameter2], k_factor2)
    
    # Calculate clamping force for both joints
    clamping_force1 = calculate_clamping_force(preload1, num_fasteners1)
    clamping_force2 = calculate_clamping_force(preload2, num_fasteners2)
    
    # Calculate equivalent strength for both joints
    equivalent_strength1 = calculate_equivalent_strength(clamping_force1, tensile_stress_areas[diameter1])
    equivalent_strength2 = calculate_equivalent_strength(clamping_force2, tensile_stress_areas[diameter2])
    
    # Calculate strength ratio
    strength_ratio = (equivalent_strength2 / equivalent_strength1) * 100
    
    # Determine pass/fail result
    result = "PASS" if strength_ratio <= 60 else "FAIL"
    
    # Display results
    st.subheader("Results")
    st.write(f"Joint 1 Preload: {preload1:.2f} lbf")
    st.write(f"Joint 1 Clamping Force: {clamping_force1:.2f} lbf")
    st.write(f"Joint 1 Equivalent Strength: {equivalent_strength1:.2f} ksi")
    st.write(f"Joint 1 Material Strength (UTS): {fastener_grades[grade1]['UTS']} psi")
    
    st.write(f"Joint 2 Preload: {preload2:.2f} lbf")
    st.write(f"Joint 2 Clamping Force: {clamping_force2:.2f} lbf")
    st.write(f"Joint 2 Equivalent Strength: {equivalent_strength2:.2f} ksi")
    st.write(f"Joint 2 Material Strength (UTS): {fastener_grades[grade2]['UTS']} psi")
    
    st.write(f"Strength Ratio: {strength_ratio:.2f}%")
    st.write(f"Result: {result}")
    
    # Display formulas used
    st.subheader("Formulas Used")
    st.latex(r"	ext{Preload} = rac{	ext{Torque} 	imes 12}{k 	imes 	ext{Diameter}}")
    st.latex(r"	ext{Clamping Force} = 	ext{Preload} 	imes 	ext{Quantity}")
    st.latex(r"	ext{Equivalent Strength} = rac{	ext{Clamping Force}}{	ext{Tensile Stress Area}} \div 1000")
    st.latex(r"	ext{Strength Ratio} = \left( rac{	ext{Joint 2 Strength}}{	ext{Joint 1 Strength}} ight) 	imes 100")
    
    # Display step-by-step calculations
    st.subheader("Step-by-Step Calculations")
    st.write(f"Joint 1 Preload Calculation: ({torque1} * 12) / ({k_factor1} * {tensile_stress_areas[diameter1]}) = {preload1:.2f} lbf")
    st.write(f"Joint 1 Clamping Force Calculation: {preload1:.2f} * {num_fasteners1} = {clamping_force1:.2f} lbf")
    st.write(f"Joint 1 Equivalent Strength Calculation: ({clamping_force1:.2f} / {tensile_stress_areas[diameter1]}) / 1000 = {equivalent_strength1:.2f} ksi")
    
    st.write(f"Joint 2 Preload Calculation: ({torque2} * 12) / ({k_factor2} * {tensile_stress_areas[diameter2]}) = {preload2:.2f} lbf")
    st.write(f"Joint 2 Clamping Force Calculation: {preload2:.2f} * {num_fasteners2} = {clamping_force2:.2f} lbf")
    st.write(f"Joint 2 Equivalent Strength Calculation: ({clamping_force2:.2f} / {tensile_stress_areas[diameter2]}) / 1000 = {equivalent_strength2:.2f} ksi")
    
    st.write(f"Strength Ratio Calculation: ({equivalent_strength2:.2f} / {equivalent_strength1:.2f}) * 100 = {strength_ratio:.2f}%")
