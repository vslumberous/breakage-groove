import streamlit as st

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

fastener_grades = {'A307B': {'strength': 60, 'type': 'Ultimate Tensile Strength'}, 'A193 B7': {'strength': 125, 'type': 'Yield Strength'}, 'A193 B7M': {'strength': 100, 'type': 'Yield Strength'}, 'A193 B8': {'strength': 75, 'type': 'Ultimate Tensile Strength'}, 'A193 B8 Cl 1': {'strength': 80, 'type': 'Ultimate Tensile Strength'}, 'A193 B8M Cl 1': {'strength': 80, 'type': 'Ultimate Tensile Strength'}, 'A574': {'strength': 170, 'type': 'Ultimate Tensile Strength'}, 'A320 L7': {'strength': 125, 'type': 'Yield Strength'}, 'A320 L7M': {'strength': 100, 'type': 'Yield Strength'}, 'A193 B8 Cl 2': {'strength_by_diameter': {'≤0.75': 125, '>0.75': 115}, 'type': 'Ultimate Tensile Strength'}, 'A193 B8M Cl 2': {'strength_by_diameter': {'≤0.75': 125, '>0.75': 115}, 'type': 'Ultimate Tensile Strength'}}

def get_strength(grade, diameter):
    if "strength_by_diameter" in fastener_grades[grade]:
        return (
            fastener_grades[grade]["strength_by_diameter"]["≤0.75"]
            if diameter <= 0.75
            else fastener_grades[grade]["strength_by_diameter"][">0.75"]
        )
    return fastener_grades[grade]["strength"]

def get_type(grade):
    return fastener_grades[grade]["type"]

st.title("Bolted Joint Strength Comparator")

st.header("Joint 1")
dia1_label = st.selectbox("Fastener Size (Joint 1)", list(unc_sizes.keys()), index=7)
dia1, tpi1 = unc_sizes[dia1_label]
qty1 = st.number_input("Number of Fasteners (Joint 1)", 1, value=8)
grade1 = st.selectbox("Fastener Grade (Joint 1)", list(fastener_grades.keys()), index=1)
strength1 = get_strength(grade1, dia1)
type1 = get_type(grade1)
torque1 = st.number_input("Torque (ft-lb) (Joint 1)", value=80, format="%d")
k1 = st.number_input("k-factor (Joint 1)", value=0.17)
st.write(f"Material Strength: {strength1} ksi ({type1})")
st.write(f"Thread Pitch: {1 / tpi1:.4f} in")

st.header("Joint 2")
dia2_label = st.selectbox("Fastener Size (Joint 2)", list(unc_sizes.keys()), index=6)
dia2, tpi2 = unc_sizes[dia2_label]
qty2 = st.number_input("Number of Fasteners (Joint 2)", 1, value=4)
grade2 = st.selectbox("Fastener Grade (Joint 2)", list(fastener_grades.keys()), index=0)
strength2 = get_strength(grade2, dia2)
type2 = get_type(grade2)
torque2 = st.number_input("Torque (ft-lb) (Joint 2)", value=50, format="%d")
k2 = st.number_input("k-factor (Joint 2)", value=0.17)
st.write(f"Material Strength: {strength2} ksi ({type2})")
st.write(f"Thread Pitch: {1 / tpi2:.4f} in")

if st.button("Calculate"):
    preload1 = (torque1 * 12) / (k1 * dia1)
    preload2 = (torque2 * 12) / (k2 * dia2)

    clamp1 = preload1 * qty1
    clamp2 = preload2 * qty2

    eq1 = clamp1 * strength1
    eq2 = clamp2 * strength2

    ratio = (eq2 / eq1) * 100 if eq1 else 0
    result = "PASS" if ratio <= 60 else "FAIL"

    st.subheader("🧮 Calculation Details")

    st.markdown("### 📐 Formulas")
    st.latex(r"\text{Preload} = \frac{\text{Torque} \times 12}{k \times \text{Diameter}}")
    st.latex(r"\text{Clamping Force} = \text{Preload} \times \text{Quantity}")
    st.latex(r"\text{Strength} = \text{Clamping Force} \times \text{Material Strength}")
    st.latex(r"\text{Ratio} = \left( \frac{\text{Joint 2 Strength}}{\text{Joint 1 Strength}} \right) \times 100")

    st.markdown("### 🧾 Step-by-Step: Joint 1")
    st.write(f"Preload = ({torque1} × 12) / ({k1} × {dia1}) = {preload1:.2f} lb")
    st.write(f"Clamping Force = {preload1:.2f} × {qty1} = {clamp1:.2f} lb")
    st.write(f"Strength = {clamp1:.2f} × {strength1} ksi = {eq1:.2f}")

    st.markdown("### 🧾 Step-by-Step: Joint 2")
    st.write(f"Preload = ({torque2} × 12) / ({k2} × {dia2}) = {preload2:.2f} lb")
    st.write(f"Clamping Force = {preload2:.2f} × {qty2} = {clamp2:.2f} lb")
    st.write(f"Strength = {clamp2:.2f} × {strength2} ksi = {eq2:.2f}")

    st.markdown("### 🧮 Strength Ratio")
    st.write(f"Ratio = ({eq2:.2f} / {eq1:.2f}) × 100 = {ratio:.2f}%")

    if result == "PASS":
        st.success("✅ PASS: Joint 2 is within 60% strength of Joint 1")
    else:
        st.error("❌ FAIL: Joint 2 exceeds 60% of Joint 1 strength")
