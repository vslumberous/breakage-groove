
import streamlit as st

# UNC fastener size mapping to decimal diameters
unc_sizes = {
    "1/2-13": 0.5,
    "5/8"-11": 0.625,
    "3/4"-10": 0.75,
    "7/8"-9": 0.875,
    "1"-8": 1.0,
    "1 1/8"-8": 1.125
}

# Predefined fastener grades with automatic strength assignment
fastener_grades = {
    "ASTM A193": 125000,
    "ASTM A320": 105000,
    "ASTM A307": 60000
}

# Function to calculate preload
def calculate_preload(torque, diameter, k_factor):
    return (torque * 12) / (k_factor * diameter)

# Function to calculate clamping force
def calculate_clamping_force(preload, quantity):
    return preload * quantity

# Function to calculate equivalent strength
def calculate_equivalent_strength(clamping_force, material_strength):
    return clamping_force * material_strength

# Function to calculate strength ratio
def calculate_strength_ratio(strength1, strength2):
    return (strength2 / strength1) * 100

# Streamlit app
st.title("Bolted Joint Analysis")

st.header("Joint 1")
diameter1 = st.selectbox("Fastener Diameter", list(unc_sizes.keys()))
tpi1 = st.number_input("Threads per Inch (TPI)", value=13, step=1)
quantity1 = st.number_input("Number of Fasteners", value=1, step=1)
grade1 = st.selectbox("Fastener Grade", list(fastener_grades.keys()))
torque1 = st.number_input("Torque (ft-lb)", value=0, step=1)
k_factor1 = st.number_input("k-factor", value=0.17)

st.header("Joint 2")
diameter2 = st.selectbox("Fastener Diameter", list(unc_sizes.keys()), key="joint2")
tpi2 = st.number_input("Threads per Inch (TPI)", value=13, step=1, key="joint2")
quantity2 = st.number_input("Number of Fasteners", value=1, step=1, key="joint2")
grade2 = st.selectbox("Fastener Grade", list(fastener_grades.keys()), key="joint2")
torque2 = st.number_input("Torque (ft-lb)", value=0, step=1, key="joint2")
k_factor2 = st.number_input("k-factor", value=0.17, key="joint2")

if st.button("Calculate"):
    diameter1 = unc_sizes[diameter1]
    diameter2 = unc_sizes[diameter2]
    material_strength1 = fastener_grades[grade1]
    material_strength2 = fastener_grades[grade2]

    preload1 = calculate_preload(torque1, diameter1, k_factor1)
    preload2 = calculate_preload(torque2, diameter2, k_factor2)

    clamping_force1 = calculate_clamping_force(preload1, quantity1)
    clamping_force2 = calculate_clamping_force(preload2, quantity2)

    strength1 = calculate_equivalent_strength(clamping_force1, material_strength1)
    strength2 = calculate_equivalent_strength(clamping_force2, material_strength2)

    strength_ratio = calculate_strength_ratio(strength1, strength2)

    result = "PASS" if strength_ratio <= 60 else "FAIL"

    st.subheader("Results")
    st.write(f"Preload for Joint 1: {preload1:.2f} lbs")
    st.write(f"Preload for Joint 2: {preload2:.2f} lbs")
    st.write(f"Total Clamping Force for Joint 1: {clamping_force1:.2f} lbs")
    st.write(f"Total Clamping Force for Joint 2: {clamping_force2:.2f} lbs")
    st.write(f"Equivalent Strength for Joint 1: {strength1:.2f} psi")
    st.write(f"Equivalent Strength for Joint 2: {strength2:.2f} psi")
    st.write(f"Strength Ratio: {strength_ratio:.2f}%")
    st.write(f"Result: {result}")

    st.subheader("Calculations Performed")
    st.markdown("""
    **Preload**:  
    $$ \text{Preload} = \frac{\text{Torque} \times 12}{k \times \text{Diameter}} $$

    **Clamping Force**:  
    $$ \text{Clamping Force} = \text{Preload} \times \text{Quantity} $$

    **Equivalent Strength**:  
    $$ \text{Equivalent Strength} = \text{Clamping Force} \times \text{Material Strength} $$

    **Strength Ratio**:  
    $$ \text{Strength Ratio} = \left( \frac{\text{Joint 2 Strength}}{\text{Joint 1 Strength}} \right) \times 100 $$

    **Pass/Fail**:  
    - **PASS** if strength ratio ≤ 60%
    - **FAIL** otherwise
    """)
