import streamlit as st

# UNC sizes with corresponding diameters in inches and threads per inch (TPI)
unc_sizes = {
    "1/4-20": (0.25, 20),
    "5/16-18": (0.3125, 18),
    "3/8-16": (0.375, 16),
    "7/16-14": (0.4375, 14),
    "1/2-13": (0.5, 13),
    "9/16-12": (0.5625, 12),
    "5/8-11": (0.625, 11),
    "3/4-10": (0.75, 10),
    "7/8-9": (0.875, 9),
    "1-8": (1.0, 8),
    "1 1/8-7": (1.125, 7),
    "1 1/4-7": (1.25, 7)
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

# Joint 1 inputs
st.header("Joint 1")
diameter1_label = st.selectbox("Fastener Size (Joint 1)", list(unc_sizes.keys()), index=7, key="joint1_diameter")
diameter1, tpi1 = unc_sizes[diameter1_label]
quantity1 = st.number_input("Number of Fasteners (Joint 1)", min_value=1, value=8, key="joint1_qty")
grade1 = st.selectbox("Fastener Grade (Joint 1)", list(fastener_grades.keys()), index=1, key="joint1_grade")
material_strength1 = fastener_grades[grade1]
st.write(f"Material Strength (Joint 1): {material_strength1} ksi")
st.write(f"Thread Pitch (Joint 1): {1 / tpi1:.4f} in")

torque1 = st.number_input("Torque (ft-lb) (Joint 1)", value=80, format="%d", key="joint1_torque")
k_factor1 = st.number_input("k-factor (Joint 1)", value=0.17, key="joint1_k")

# Joint 2 inputs
st.header("Joint 2")
diameter2_label = st.selectbox("Fastener Size (Joint 2)", list(unc_sizes.keys()), index=6, key="joint2_diameter")
diameter2, tpi2 = unc_sizes[diameter2_label]
quantity2 = st.number_input("Number of Fasteners (Joint 2)", min_value=1, value=4, key="joint2_qty")
grade2 = st.selectbox("Fastener Grade (Joint 2)", list(fastener_grades.keys()), index=0, key="joint2_grade")
material_strength2 = fastener_grades[grade2]
st.write(f"Material Strength (Joint 2): {material_strength2} ksi")
st.write(f"Thread Pitch (Joint 2): {1 / tpi2:.4f} in")

torque2 = st.number_input("Torque (ft-lb) (Joint 2)", value=50, format="%d", key="joint2_torque")
k_factor2 = st.number_input("k-factor (Joint 2)", value=0.17, key="joint2_k")

if st.button("Calculate"):
    # Preload calculations
    preload1 = (torque1 * 12) / (k_factor1 * diameter1)
    preload2 = (torque2 * 12) / (k_factor2 * diameter2)

    # Clamping force
    clamp_force1 = preload1 * quantity1
    clamp_force2 = preload2 * quantity2

    # Equivalent strength
    strength1 = clamp_force1 * material_strength1
    strength2 = clamp_force2 * material_strength2

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
    st.write(f"Preload = ({torque1} × 12) / ({k_factor1} × {diameter1}) = {preload1:.2f} lb")
    st.write(f"Clamping Force = {preload1:.2f} × {quantity1} = {clamp_force1:.2f} lb")
    st.write(f"Equivalent Strength = {clamp_force1:.2f} × {material_strength1} ksi = {strength1:.2f}")

    st.markdown("### Joint 2 Calculations")
    st.write(f"Preload = ({torque2} × 12) / ({k_factor2} × {diameter2}) = {preload2:.2f} lb")
    st.write(f"Clamping Force = {preload2:.2f} × {quantity2} = {clamp_force2:.2f} lb")
    st.write(f"Equivalent Strength = {clamp_force2:.2f} × {material_strength2} ksi = {strength2:.2f}")

    st.markdown("### Final Evaluation")
    st.write(f"Strength Ratio = ({strength2:.2f} / {strength1:.2f}) × 100 = {ratio:.2f}%")
    if result == "PASS":
        st.success("PASS: Joint 2 strength is within 60% of Joint 1.")
    else:
        st.error("FAIL: Joint 2 strength exceeds 60% of Joint 1.")
