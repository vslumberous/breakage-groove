# We'll now modify the script based on the user's requests:
# - Remove TPI input; instead, derive it from selected fastener diameter.
# - Use a single shared diameter input for both joints.
# - Add a comprehensive list of materials with their corresponding strength values.
# - Update the output section to include step-by-step calculations with formulas.

# First, we'll adjust the original code accordingly
updated_lines = []

# Define the new list of fastener grades with their strength values in ksi
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

# Rebuild the script with modifications
for line in lines:
    if 'tpi1 =' in line or 'tpi2 =' in line:
        continue  # Remove TPI lines
    elif 'st.header("Joint 1")' in line:
        updated_lines.append(line)
        updated_lines.append('diameter = st.selectbox("Fastener Diameter (UNC)", list(unc_sizes.keys()))\n')
    elif 'diameter1 =' in line or 'diameter2 =' in line:
        continue  # Remove individual diameter inputs, now shared
    elif 'st.header("Joint 2")' in line:
        updated_lines.append(line)
    elif 'grade1 =' in line:
        updated_lines.append('grade1 = st.selectbox("Fastener Grade (Joint 1)", list(fastener_grades.keys()))\n')
    elif 'grade2 =' in line:
        updated_lines.append('grade2 = st.selectbox("Fastener Grade (Joint 2)", list(fastener_grades.keys()), key="joint2_grade")\n')
    else:
        updated_lines.append(line)

# Append updated calculations and step-by-step output
output_block = f"""
    diameter_val = unc_sizes[diameter]
    preload1 = (torque1 * 12) / (k_factor1 * diameter_val)
    preload2 = (torque2 * 12) / (k_factor2 * diameter_val)

    clamp_force1 = preload1 * quantity1
    clamp_force2 = preload2 * quantity2

    strength1 = clamp_force1 * fastener_grades[grade1]
    strength2 = clamp_force2 * fastener_grades[grade2]

    ratio = (strength2 / strength1) * 100
    result = "PASS" if ratio <= 60 else "FAIL"

    st.subheader("Calculation Details")
    st.markdown("### Formulas Used")
    st.markdown("**Preload** = (Torque × 12) / (k-factor × Diameter)")
    st.markdown("**Clamping Force** = Preload × Number of Fasteners")
    st.markdown("**Equivalent Strength** = Clamping Force × Material Strength")
    st.markdown("**Strength Ratio** = (Joint 2 Strength / Joint 1 Strength) × 100")

    st.markdown("### Joint 1 Calculations")
    st.write(f"Preload = ({{torque1}} × 12) / ({{k_factor1}} × {{diameter_val}}) = {{preload1:.2f}} lb")
    st.write(f"Clamping Force = {{preload1:.2f}} × {{quantity1}} = {{clamp_force1:.2f}} lb")
    st.write(f"Equivalent Strength = {{clamp_force1:.2f}} × {{fastener_grades[grade1]}} ksi = {{strength1:.2f}}")

    st.markdown("### Joint 2 Calculations")
    st.write(f"Preload = ({{torque2}} × 12) / ({{k_factor2}} × {{diameter_val}}) = {{preload2:.2f}} lb")
    st.write(f"Clamping Force = {{preload2:.2f}} × {{quantity2}} = {{clamp_force2:.2f}} lb")
    st.write(f"Equivalent Strength = {{clamp_force2:.2f}} × {{fastener_grades[grade2]}} ksi = {{strength2:.2f}}")

    st.markdown("### Final Evaluation")
    st.write(f"Strength Ratio = ({{strength2:.2f}} / {{strength1:.2f}}) × 100 = {{ratio:.2f}}%")
    st.success("PASS: Joint 2 strength is within allowable limits.") if result == "PASS" else st.error("FAIL: Joint 2 strength exceeds 60% of Joint 1.")
"""

# Inject output block after the line where material strengths are extracted
for i, line in enumerate(updated_lines):
    if "material_strength2 =" in line:
        insert_index = i + 1
        break

updated_lines = updated_lines[:insert_index] + [output_block] + updated_lines[insert_index:]

# Save the final version
final_script_path = "/mnt/data/bolted_joint_comparator_final.py"
with open(final_script_path, "w") as f:
    f.writelines(updated_lines)

final_script_path
