
import streamlit as st

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

# Mapping of tensile stress areas for UNC fasteners
tensile_stress_areas = {
    "1/2-13": 0.1419,
    "5/8-11": 0.226,
    "3/4-10": 0.334,
    "7/8-9": 0.462,
    "1-8": 0.606,
    "1 1/8-8": 0.763
}

# Mapping of material strengths in psi
material_strengths = {
    "A193 B7": 125000,
    "A193 B7M": 105000,
    "A193 B8": 75000,
    "A193 B8M": 75000,
    "A307 Gr. B": 60000,
    "A574": 170000
}

# Streamlit app
st.title("Bolted Joint Analysis App")

# Input fields for Joint 1
st.header("Joint 1")
fastener_1 = st.selectbox("Fastener Diameter (UNC standard)", list(tensile_stress_areas.keys()), key="joint1_fastener")
num_fasteners_1 = st.number_input("Number of Fasteners", min_value=1, step=1, key="joint1_num_fasteners")
material_1 = st.selectbox("Fastener Grade", list(material_strengths.keys()), key="joint1_material")
torque_1 = st.number_input("Torque (ft-lb)", min_value=0.0, step=0.1, key="joint1_torque")
k_factor_1 = st.number_input("k-factor (friction factor)", value=0.17, step=0.01, key="joint1_k_factor")

# Input fields for Joint 2
st.header("Joint 2")
fastener_2 = st.selectbox("Fastener Diameter (UNC standard)", list(tensile_stress_areas.keys()), key="joint2_fastener")
num_fasteners_2 = st.number_input("Number of Fasteners", min_value=1, step=1, key="joint2_num_fasteners")
material_2 = st.selectbox("Fastener Grade", list(material_strengths.keys()), key="joint2_material")
torque_2 = st.number_input("Torque (ft-lb)", min_value=0.0, step=0.1, key="joint2_torque")
k_factor_2 = st.number_input("k-factor (friction factor)", value=0.17, step=0.01, key="joint2_k_factor")

# Calculate button
if st.button("Calculate"):
    # Calculate preload for both joints
    preload_1 = calculate_preload(torque_1, k_factor_1, tensile_stress_areas[fastener_1])
    preload_2 = calculate_preload(torque_2, k_factor_2, tensile_stress_areas[fastener_2])
    
    # Calculate clamping force for both joints
    clamping_force_1 = calculate_clamping_force(preload_1, num_fasteners_1)
    clamping_force_2 = calculate_clamping_force(preload_2, num_fasteners_2)
    
    # Calculate equivalent strength for both joints
    equivalent_strength_1 = calculate_equivalent_strength(clamping_force_1, tensile_stress_areas[fastener_1])
    equivalent_strength_2 = calculate_equivalent_strength(clamping_force_2, tensile_stress_areas[fastener_2])
    
    # Calculate strength ratio
    strength_ratio = calculate_strength_ratio(equivalent_strength_1, equivalent_strength_2)
    
    # Determine pass/fail result
    result = "PASS" if strength_ratio <= 60 else "FAIL"
    
    # Display results
    st.subheader("Results")
    st.write(f"Preload (Joint 1): {preload_1:.2f} lbf")
    st.write(f"Preload (Joint 2): {preload_2:.2f} lbf")
    st.write(f"Clamping Force (Joint 1): {clamping_force_1:.2f} lbf")
    st.write(f"Clamping Force (Joint 2): {clamping_force_2:.2f} lbf")
    st.write(f"Equivalent Strength (Joint 1): {equivalent_strength_1:.2f} ksi")
    st.write(f"Equivalent Strength (Joint 2): {equivalent_strength_2:.2f} ksi")
    st.write(f"Strength Ratio: {strength_ratio:.2f}%")
    st.write(f"Result: {result}")
    
    # Display formulas
    st.subheader("Formulas Used")
    st.latex(r"\text{Preload} = \frac{\text{Torque} \times 12}{k \times \text{Diameter}}")
    st.latex(r"\text{Clamping Force} = \text{Preload} \times \text{Quantity}")
    st.latex(r"\text{Equivalent Strength} = \frac{\text{Clamping Force}}{\text{Tensile Stress Area}} \div 1000")
    st.latex(r"\text{Strength Ratio} = \left( \frac{\text{Joint 2 Strength}}{\text{Joint 1 Strength}} \right) \times 100")
