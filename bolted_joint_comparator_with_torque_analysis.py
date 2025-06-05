import streamlit as st

# UNC sizes with corresponding diameters in inches and threads per inch (TPI)
unc_sizes = {
    "1/4-20": (0.25, 20),
    "5/16-18": (0.3125, 18),
    "3/8-16": 0.375,
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

# Fastener material strengths and whether it's yield or ultimate tensile strength
fastener_grades = {
    "A307B": {"strength": 60, "type": "Ultimate Tensile Strength"},
    "A193 B7": {"strength": 125, "type": "Yield Strength"},
    "A193 B7M": {"strength": 100, "type": "Yield Strength"},
    "A193 B8": {"strength": 75, "type": "Ultimate Tensile Strength"},
    "A193 B8 Cl 1": {"strength": 80, "type": "Ultimate Tensile Strength"},
    "A193 B8M Cl 1": {"strength": 80, "type": "Ultimate Tensile Strength"},
    "A574": {"strength": 170, "type": "Ultimate Tensile Strength"},
    "A320 L7": {"strength": 125, "type": "Yield Strength"},
    "A320 L7M": {"strength": 100, "type": "Yield Strength"}
}

st.title("Bolted Joint Strength Comparator")

# Joint 1 inputs
st.header("Joint 1")
diameter1_label = st.selectbox("Fastener Size (Joint 1)", list(unc_sizes.keys()), index=7, key="joint1_diameter")
diameter1, tpi1 = unc_sizes[diameter1_label]
quantity1 = st.number_input("Number of Fasteners (Joint 1)", min_value=1, value=8, key="joint1_qty")
grade1 = st.selectbox("Fastener Grade (Joint 1)", list(fastener_grades.keys()), index=1, key="joint1_grade")
material_strength1 = fastener_grades[grade1]["strength"]
material_type1 = fastener_grades[grade1]["type"]
st.write(f"Material Strength (Joint 1): {material_strength1} ksi ({material_type1})")
st.write(f"Thread Pitch (Joint 1): {1 / tpi1:.4f} in")

torque1 = st.number_input("Torque (ft-lb) (Joint 1)", value=80, format="%d", key="joint1_torque")
k_factor1 = st.number_input("k-factor (Joint 1)", value=0.17, key="joint1_k")

# Joint 2 inputs
st.header("Joint 2")
diameter2_label = st.selectbox("Fastener Size (Joint 2)", list(unc_sizes.keys()), index=6, key="joint2_diameter")
diameter2, tpi2 = unc_sizes[diameter2_label]
quantity2 = st.number_input("Number of Fasteners (Joint 2)", min_value=1, value=4, key="joint2_qty")
grade2 = st.selectbox("Fastener Grade (Joint 2)", list(fastener_grades.keys()), index=0, key="joint2_grade")
material_strength2 = fastener_grades[grade2]["strength"]
material_type2 = fastener_grades[grade2]["type"]
st.write(f"Material Strength (Joint 2): {material_strength2} ksi ({material_type2})")
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
    st.write(f"Equivalent Strength = {clamp_force1:.2f} × {material_strength1} ksi ({material_type1}) = {strength1:.2f}")

    st.markdown("### Joint 2 Calculations")
    st.write(f"Preload = ({torque2} × 12) / ({k_factor2} × {diameter2}) = {preload2:.2f} lb")
    st.write(f"Clamping Force = {preload2:.2f} × {quantity2} = {clamp_force2:.2f} lb")
    st.write(f"Equivalent Strength = {clamp_force2:.2f} × {material_strength2} ksi ({material_type2}) = {strength2:.2f}")

    st.markdown("### Final Evaluation")
    st.write(f"Strength Ratio = ({strength2:.2f} / {strength1:.2f}) × 100 = {ratio:.2f}%")
    if result == "PASS":
        st.success("PASS: Joint 2 strength is within 60% of Joint 1.")
    else:
        st.error("FAIL: Joint 2 strength exceeds 60% of Joint 1.")

        st.markdown("### Suggestions to Improve Joint 2 Performance")

        # Material improvement suggestions
        stronger_materials = [mat for mat, props in fastener_grades.items()
                              if props["strength"] > material_strength2]
        weaker_materials = [mat for mat, props in fastener_grades.items()
                              if props["strength"] < material_strength2]

        if stronger_materials:
            st.write("🔧 Try using a stronger material for Joint 2 such as:")
            for mat in stronger_materials:
                st.write(f"- {mat} ({fastener_grades[mat]['strength']} ksi, {fastener_grades[mat]['type']})")

        if diameter2_label != "1 1/4-7":
            st.write("🔧 Consider using a slightly larger fastener size for Joint 2 to increase clamping force.")
        elif diameter2_label != "1/4-20":
            st.write("🔧 Alternatively, use a smaller fastener size in Joint 1 to balance the ratio.")

        st.write("🔧 You might also increase the applied torque for Joint 2 to increase its preload and strength.")
        # Estimate new preload with 10% more torque
        suggested_torque2 = torque2 * 1.10
        new_preload2 = (suggested_torque2 * 12) / (k_factor2 * diameter2)
        new_clamp_force2 = new_preload2 * quantity2
        new_strength2 = new_clamp_force2 * material_strength2
        yield_util_percent = (new_strength2 / (clamp_force2 * material_strength2)) * 100

        st.markdown("### Estimated Impact of Increasing Torque by 10%")
        st.write(f"New Torque: {suggested_torque2:.0f} ft-lb")
        st.write(f"Estimated Preload: {new_preload2:.2f} lb")
        st.write(f"Estimated Clamping Force: {new_clamp_force2:.2f} lb")
        st.write(f"Estimated Strength: {new_strength2:.2f}")
        st.write(f"Strength Increase: {yield_util_percent:.1f}% over current Joint 2 strength")

        if yield_util_percent >= 100:
            st.warning("⚠️ This may exceed the fastener's rated strength. Use caution and validate before applying.")
        else:
            st.success("✅ This adjustment may bring the joint within acceptable limits.")


