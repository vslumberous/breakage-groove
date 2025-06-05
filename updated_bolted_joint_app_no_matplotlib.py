
import streamlit as st

# UNC fastener size mapping to decimal diameters
unc_sizes = {
    "1/2\"-13": 0.5,
    "9/16\"-12": 0.5625,
    "5/8\"-11": 0.625,
    "3/4\"-10": 0.75,
    "7/8\"-9": 0.875,
    "1\"-8": 1.0,
    "1 1/8\"-8": 1.125
}

# Predefined fastener grades with material strength (psi)
fastener_grades = {
    "ASTM A193": 125000,
    "ASTM A320": 105000,
    "ASTM A307": 60000
}

# Streamlit app
st.title("Bolted Joint Analysis")

# Joint 1 inputs
st.header("Joint 1")
diameter_1 = st.selectbox("Fastener Diameter (UNC)", list(unc_sizes.keys()))
tpi_1 = st.number_input("Threads per Inch (TPI)", value=13, step=1)
quantity_1 = st.number_input("Number of Fasteners", value=1, step=1)
grade_1 = st.selectbox("Fastener Grade", list(fastener_grades.keys()))
torque_1 = st.number_input("Torque (ft-lb)", value=0, step=1)
k_factor_1 = st.number_input("k-factor", value=0.17)

# Joint 2 inputs
st.header("Joint 2")
diameter_2 = st.selectbox("Fastener Diameter (UNC)", list(unc_sizes.keys()), key="joint2")
tpi_2 = st.number_input("Threads per Inch (TPI)", value=13, step=1, key="joint2")
quantity_2 = st.number_input("Number of Fasteners", value=1, step=1, key="joint2")
grade_2 = st.selectbox("Fastener Grade", list(fastener_grades.keys()), key="joint2")
torque_2 = st.number_input("Torque (ft-lb)", value=0, step=1, key="joint2")
k_factor_2 = st.number_input("k-factor", value=0.17, key="joint2")

# Calculations
def calculate_preload(torque, diameter, k_factor):
    return (torque * 12) / (k_factor * diameter)

def calculate_clamping_force(preload, quantity):
    return preload * quantity

def calculate_equivalent_strength(clamping_force, material_strength):
    return clamping_force * material_strength

diameter_1_decimal = unc_sizes[diameter_1]
diameter_2_decimal = unc_sizes[diameter_2]

preload_1 = calculate_preload(torque_1, diameter_1_decimal, k_factor_1)
clamping_force_1 = calculate_clamping_force(preload_1, quantity_1)
equivalent_strength_1 = calculate_equivalent_strength(clamping_force_1, fastener_grades[grade_1])

preload_2 = calculate_preload(torque_2, diameter_2_decimal, k_factor_2)
clamping_force_2 = calculate_clamping_force(preload_2, quantity_2)
equivalent_strength_2 = calculate_equivalent_strength(clamping_force_2, fastener_grades[grade_2])

# Check for zero to avoid division by zero error
if equivalent_strength_1 != 0:
    strength_ratio = (equivalent_strength_2 / equivalent_strength_1) * 100
else:
    strength_ratio = 0

result = "PASS" if strength_ratio <= 60 else "FAIL"

# Display results
st.subheader("Results")
st.write(f"Preload for Joint 1: {preload_1:.2f} lbs")
st.write(f"Clamping Force for Joint 1: {clamping_force_1:.2f} lbs")
st.write(f"Equivalent Strength for Joint 1: {equivalent_strength_1:.2f} psi")

st.write(f"Preload for Joint 2: {preload_2:.2f} lbs")
st.write(f"Clamping Force for Joint 2: {clamping_force_2:.2f} lbs")
st.write(f"Equivalent Strength for Joint 2: {equivalent_strength_2:.2f} psi")

st.write(f"Strength Ratio: {strength_ratio:.2f}%")
st.write(f"Result: {result}")

# Display calculation summary
st.subheader("Calculation Summary")
st.markdown("""
### Formulas Used
1. **Preload**:  
   $$ \text{Preload} = \frac{\text{Torque} \times 12}{k \times \text{Diameter}} $$
2. **Clamping Force**:  
   $$ \text{Clamping Force} = \text{Preload} \times \text{Quantity} $$
3. **Equivalent Strength**:  
   $$ \text{Equivalent Strength} = \text{Clamping Force} \times \text{Material Strength} $$
4. **Strength Ratio**:  
   $$ \text{Strength Ratio} = \left( \frac{\text{Joint 2 Strength}}{\text{Joint 1 Strength}} \right) \times 100 $$
5. **Pass/Fail**:  
   - **PASS** if strength ratio ≤ 60%
   - **FAIL** otherwise
""")
