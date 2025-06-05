
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

# Define material strengths in ksi
material_strengths = {
    "A193 B7": 125,
    "A193 B7M": 105,
    "A193 B8": 75,
    "A193 B8M": 75,
    "A307 Gr. B": 60,
    "A574": 170
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
def calculate_strength_ratio(joint1_strength, joint2_strength):
    return (joint2_strength / joint1_strength) * 100

# Streamlit app
st.title("Bolted Joint Analysis")

# Input fields for Joint 1
st.header("Joint 1")
fastener_size_1 = st.selectbox("Fastener Size (UNC)", list(tensile_stress_areas.keys()), key="fastener_size_1")
num_fasteners_1 = st.number_input("Number of Fasteners", min_value=1, key="num_fasteners_1")
fastener_grade_1 = st.selectbox("Fastener Grade", list(material_strengths.keys()), key="fastener_grade_1")
torque_1 = st.number_input("Torque (ft-lb)", min_value=0.0, key="torque_1")
k_factor_1 = st.number_input("k-factor (friction factor)", min_value=0.0, value=0.17, key="k_factor_1")

# Input fields for Joint 2
st.header("Joint 2")
fastener_size_2 = st.selectbox("Fastener Size (UNC)", list(tensile_stress_areas.keys()), key="fastener_size_2")
num_fasteners_2 = st.number_input("Number of Fasteners", min_value=1, key="num_fasteners_2")
fastener_grade_2 = st.selectbox("Fastener Grade", list(material_strengths.keys()), key="fastener_grade_2")
torque_2 = st.number_input("Torque (ft-lb)", min_value=0.0, key="torque_2")
k_factor_2 = st.number_input("k-factor (friction factor)", min_value=0.0, value=0.17, key="k_factor_2")

# Calculate and display results
if st.button("Calculate"):
    # Joint 1 calculations
    diameter_1 = float(fastener_size_1.split('-')[0].replace('/', '.'))
    preload_1 = calculate_preload(torque_1, k_factor_1, diameter_1)
    clamping_force_1 = calculate_clamping_force(preload_1, num_fasteners_1)
    tensile_stress_area_1 = tensile_stress_areas[fastener_size_1]
    equivalent_strength_1 = calculate_equivalent_strength(clamping_force_1, tensile_stress_area_1)
    
    # Joint 2 calculations
    diameter_2 = float(fastener_size_2.split('-')[0].replace('/', '.'))
    preload_2 = calculate_preload(torque_2, k_factor_2, diameter_2)
    clamping_force_2 = calculate_clamping_force(preload_2, num_fastesters_2)
    tensile_stress_area_2 = tensile_stress_areas[fastener_size_2]
    equivalent_strength_2 = calculate_equivalent_strength(clamping_force_2, tensile_stress_area_2)
    
    # Strength ratio calculation
    strength_ratio = calculate_strength_ratio(equivalent_strength_1, equivalent_strength_2)
    result = "PASS" if strength_ratio >= 100 else "FAIL"
    
    # Display results
    st.subheader("Results")
    st.write(f"Joint 1 Preload: {preload_1:.2f} lbf")
    st.write(f"Joint 1 Clamping Force: {clamping_force_1:.2f} lbf")
    st.write(f"Joint 1 Equivalent Strength: {equivalent_strength_1:.2f} ksi")
    st.write(f"Joint 2 Preload: {preload_2:.2f} lbf")
    st.write(f"Joint 2 Clamping Force: {clamping_force_2:.2f} lbf")
    st.write(f"Joint 2 Equivalent Strength: {equivalent_strength_2:.2f} ksi")
    st.write(f"Strength Ratio: {strength_ratio:.2f}%")
    st.write(f"Result: {result}")
    
    # Display formulas
    st.subheader("Formulas Used")
    st.latex(r"\text{Preload} = \frac{\text{Torque} \times 12}{k \times \text{Diameter}}")
    st.latex(r"\text{Clamping Force} = \text{Preload} \times \text{Quantity}")
    st.latex(r"\text{Equivalent Strength (ksi)} = \frac{\text{Clamping Force (lbf)}}{\text{Tensile Stress Area (in}^2)} \div 1000")
    st.latex(r"\text{Strength Ratio} = \left( \frac{\text{Joint 2 Strength}}{\text{Joint 1 Strength}} \right) \times 100")
