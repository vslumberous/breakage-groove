
import streamlit as st
import matplotlib.pyplot as plt

# UNC fastener size mapping to decimal diameters
unc_sizes = {
    "1/2\"-13": 0.5,
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
diameter1 = st.selectbox("Fastener Diameter (UNC)", list(unc_sizes.keys()))
tpi1 = st.number_input("Threads per Inch (TPI)", value=13, step=1)
quantity1 = st.number_input("Number of Fasteners", value=1, step=1)
grade1 = st.selectbox("Fastener Grade", list(fastener_grades.keys()))
torque1 = st.number_input("Torque (ft-lb)", value=100, step=1)
k_factor1 = st.number_input("k-factor", value=0.17)

# Joint 2 inputs
st.header("Joint 2")
diameter2 = st.selectbox("Fastener Diameter (UNC)", list(unc_sizes.keys()), key="joint2")
tpi2 = st.number_input("Threads per Inch (TPI)", value=13, step=1, key="joint2")
quantity2 = st.number_input("Number of Fasteners", value=1, step=1, key="joint2")
grade2 = st.selectbox("Fastener Grade", list(fastener_grades.keys()), key="joint2")
torque2 = st.number_input("Torque (ft-lb)", value=100, step=1, key="joint2")
k_factor2 = st.number_input("k-factor", value=0.17, key="joint2")

# Calculate preload
def calculate_preload(torque, diameter, k_factor):
    return (torque * 12) / (k_factor * diameter)

preload1 = calculate_preload(torque1, unc_sizes[diameter1], k_factor1)
preload2 = calculate_preload(torque2, unc_sizes[diameter2], k_factor2)

# Calculate clamping force
clamping_force1 = preload1 * quantity1
clamping_force2 = preload2 * quantity2

# Calculate equivalent strength
equivalent_strength1 = clamping_force1 * fastener_grades[grade1]
equivalent_strength2 = clamping_force2 * fastener_grades[grade2]

# Calculate strength ratio
strength_ratio = (equivalent_strength2 / equivalent_strength1) * 100

# Determine pass/fail
result = "PASS" if strength_ratio <= 60 else "FAIL"

# Display results
st.subheader("Results")
st.write(f"Preload for Joint 1: {preload1:.2f} lbs")
st.write(f"Preload for Joint 2: {preload2:.2f} lbs")
st.write(f"Clamping Force for Joint 1: {clamping_force1:.2f} lbs")
st.write(f"Clamping Force for Joint 2: {clamping_force2:.2f} lbs")
st.write(f"Equivalent Strength for Joint 1: {equivalent_strength1:.2f} psi")
st.write(f"Equivalent Strength for Joint 2: {equivalent_strength2:.2f} psi")
st.write(f"Strength Ratio: {strength_ratio:.2f}%")
st.write(f"Result: {result}")

# Display bar chart
fig, ax = plt.subplots()
labels = ["Joint 1", "Joint 2"]
preloads = [preload1, preload2]
clamping_forces = [clamping_force1, clamping_force2]
equivalent_strengths = [equivalent_strength1, equivalent_strength2]

x = range(len(labels))
ax.bar(x, preloads, width=0.2, label="Preload", align='center')
ax.bar(x, clamping_forces, width=0.2, label="Clamping Force", align='edge')
ax.bar(x, equivalent_strengths, width=0.2, label="Equivalent Strength", align='edge')

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

st.pyplot(fig)

# Display calculation summary
st.subheader("Calculations Performed")
st.markdown("""
### Formulas and Variables

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
