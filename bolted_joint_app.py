
import streamlit as st

def calculate_preload(torque, k_factor, diameter):
    return (torque * 12) / (k_factor * diameter)

def calculate_clamping_force(preload, quantity):
    return preload * quantity

def calculate_equivalent_strength(clamping_force, material_strength):
    return clamping_force * material_strength

def main():
    st.title("Bolted Joint Analysis Tool")

    st.header("Joint 1 Parameters")
    diameter_1 = st.number_input("Fastener Diameter (inches)", key="diameter_1")
    tpi_1 = st.number_input("Threads per Inch", key="tpi_1")
    quantity_1 = st.number_input("Number of Fasteners", key="quantity_1")
    material_strength_1 = st.number_input("Material Strength (psi)", key="material_strength_1")
    torque_1 = st.number_input("Torque (ft-lb)", key="torque_1")
    k_factor_1 = st.number_input("k-factor", value=0.17, key="k_factor_1")

    st.header("Joint 2 Parameters")
    diameter_2 = st.number_input("Fastener Diameter (inches)", key="diameter_2")
    tpi_2 = st.number_input("Threads per Inch", key="tpi_2")
    quantity_2 = st.number_input("Number of Fasteners", key="quantity_2")
    material_strength_2 = st.number_input("Material Strength (psi)", key="material_strength_2")
    torque_2 = st.number_input("Torque (ft-lb)", key="torque_2")
    k_factor_2 = st.number_input("k-factor", value=0.17, key="k_factor_2")

    if st.button("Calculate"):
        preload_1 = calculate_preload(torque_1, k_factor_1, diameter_1)
        clamping_force_1 = calculate_clamping_force(preload_1, quantity_1)
        equivalent_strength_1 = calculate_equivalent_strength(clamping_force_1, material_strength_1)

        preload_2 = calculate_preload(torque_2, k_factor_2, diameter_2)
        clamping_force_2 = calculate_clamping_force(preload_2, quantity_2)
        equivalent_strength_2 = calculate_equivalent_strength(clamping_force_2, material_strength_2)

        strength_ratio = (equivalent_strength_2 / equivalent_strength_1) * 100
        result = "PASS" if strength_ratio <= 60 else "FAIL"

        st.subheader("Results")
        st.write(f"Joint 1 Equivalent Strength: {equivalent_strength_1:.2e} lbf·psi")
        st.write(f"Joint 2 Equivalent Strength: {equivalent_strength_2:.2e} lbf·psi")
        st.write(f"Strength Ratio: {strength_ratio:.2f}%")
        st.write(f"Result: {result}")

if __name__ == "__main__":
    main()
