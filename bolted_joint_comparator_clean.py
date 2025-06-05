import streamlit as st

# UNC sizes with corresponding diameters in inches
unc_sizes = {
    "1/4-20": 0.25,
    "5/16-18": 0.3125,
    "3/8-16": 0.375,
    "7/16-14": 0.4375,
    "1/2-13": 0.5,
    "9/16-12": 0.5625,
    "5/8-11": 0.625,
    "3/4-10": 0.75,
    "7/8-9": 0.875,
    "1-8": 1.0
}

# Material grades and their strengths in ksi
fastener_grades = {
    "A307B": 60,
    "A193 B7": 125,
    "A193 B7M": 100,
    "A193 B8": 75,
    "A193 B8 Cl 1": 80,
    "A193 B8M Cl 1": 80,
    "A574": 170,
    "A320 L7": 125,
    "A320 L7M": 100
}

st.title("Bolted Joint Strength Comparator")

# Shared input for both joints
st.subheader("Joint Configuration")
diameter = st.selectbox("Fastener Diameter (UNC)", list(unc_sizes.keys()))
diameter_val = unc_sizes[diameter]

# Joint 1 inputs
st.header("Joint 1")
quantity1 = st.number_input("Number of Fasteners", min_value=1, value=1)
grade1 = st.selectbox("Fastener Grade (Joint 1)", list(fastener_grades.keys()))
torque1 = st.number_input("Torque (ft-lb)", value=0.0)
k_factor1 = st.number_input("k-factor", value=0.17)

# Joint 2 inputs
st.header("Joint 2")
quantity2 = st.number_input("Number of Fasteners", min_value=1, value=1, key="joint2_quantity")
grade2 = st.selectbox("Fastener Grade (Joint 2)", list(fastener_grades.keys()), key="joint2_grade")
torque2 = st.number_input("Torque (ft-lb)", value=0.0, key="joint2_torque")
k_factor2 = st.number_input("k-factor", value=0.17, key="joint2_k_factor")

if st.button("Calculate"):
    # Preload calculations
    preload1 = (torque1 * 12) / (k_factor1 * diameter_val)
    preload2 = (torque2 * 12) / (k_factor2 * diameter_val)

    # Clamping force
    clamp_force1 = preload1 * quantity1
    clamp_force2 = preload2 * quantity2

    # Equivalent strength
    strength1 = clamp_force1 * fastener_grades[grade1]
    strength2 = clamp_force2 * fastener_grades[grade2]

    # Strength ratio and result
    ratio = (strength2 / strength1) * 100 if strength1 != 0 else 0
    result = "PASS" if ratio <= 60 else "FAIL"

    # Output details
    st.subheader("Calculation Details")
    st.markdown("### Formulas Used")
    st.markdown("**Preload** = (Torque × 12) / (k-factor × Diameter)")
    st.markdown("**Clamping Force** = Preload × Number of Fasteners")
    st.markdown("**Equivalent Strength** = Clamping Force × Material Strength (ksi)")
    st.markdown("**Strength Ratio** = (Joint 2 Strength / Joint 1 Strength) × 100")

    st.markdown("### Joint 1 Calculations")
    st.write(f"Preload = ({torque1} × 12) / ({k_factor1} × {diameter_val}) = {preload1:.2f} lb")
    st.write(f"Clamping Force = {preload1:.2f} × {quantity1} = {clamp_force1:.2f} lb")
    st.write(f"Equivalent Strength = {clamp_force1:.2f} × {fastener_grades[grade1]} ksi = {strength1:.2f}")

    st.markdown("### Joint 2 Calculations")
    st.write(f"Preload = ({torque2} × 12) / ({k_factor2} × {diameter_val}) = {preload2:.2f} lb")
    st.write(f"Clamping Force = {preload2:.2f} × {quantity2} = {clamp_force2:.2f} lb")
    st.write(f"Equivalent Strength = {clamp_force2:.2f} × {fastener_grades[grade2]} ksi = {strength2:.2f}")

    st.markdown("### Final Evaluation")
    st.write(f"Strength Ratio = ({strength2:.2f} / {strength1:.2f}) × 100 = {ratio:.2f}%")
    if result == "PASS":
        st.success("PASS: Joint 2 strength is within 60% of Joint 1.")
    else:
        st.error("FAIL: Joint 2 strength exceeds 60% of Joint 1.")
