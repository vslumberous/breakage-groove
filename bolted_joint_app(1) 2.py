
import streamlit as st

def calculate_preload(torque, k_factor, diameter):
    return (torque * 12) / (k_factor * diameter)

def calculate_clamping_force(preload, quantity):
    return preload * quantity

def calculate_equivalent_strength(clamping_force, material_strength):
    return clamping_force * material_strength

def calculate_strength_ratio(joint1_strength, joint2_strength):
    return (joint2_strength / joint1_strength) * 100

def bolted_joint_analysis(joint1, joint2):
    preload1 = calculate_preload(joint1['torque'], joint1['k_factor'], joint1['diameter'])
    preload2 = calculate_preload(joint2['torque'], joint2['k_factor'], joint2['diameter'])
    
    clamping_force1 = calculate_clamping_force(preload1, joint1['quantity'])
    clamping_force2 = calculate_clamping_force(preload2, joint2['quantity'])
    
    equivalent_strength1 = calculate_equivalent_strength(clamping_force1, joint1['material_strength'])
    equivalent_strength2 = calculate_equivalent_strength(clamping_force2, joint2['material_strength'])
    
    strength_ratio = calculate_strength_ratio(equivalent_strength1, equivalent_strength2)
    
    result = "PASS" if strength_ratio <= 60 else "FAIL"
    
    return {
        'preload1': preload1,
        'preload2': preload2,
        'clamping_force1': clamping_force1,
        'clamping_force2': clamping_force2,
        'equivalent_strength1': equivalent_strength1,
        'equivalent_strength2': equivalent_strength2,
        'strength_ratio': strength_ratio,
        'result': result
    }

st.title("Bolted Joint Analysis Tool")

st.header("Input Parameters for Joint 1")
joint1_diameter = st.number_input("Fastener Diameter (inches)", value=0.75)
joint1_tpi = st.number_input("Threads per Inch", value=10)
joint1_quantity = st.number_input("Number of Fasteners", value=8)
joint1_material_strength = st.number_input("Material Strength (psi)", value=105000)
joint1_torque = st.number_input("Torque (ft-lb)", value=80)
joint1_k_factor = st.number_input("k-factor", value=0.17)

st.header("Input Parameters for Joint 2")
joint2_diameter = st.number_input("Fastener Diameter (inches)", value=0.625)
joint2_tpi = st.number_input("Threads per Inch", value=11)
joint2_quantity = st.number_input("Number of Fasteners", value=4)
joint2_material_strength = st.number_input("Material Strength (psi)", value=60000)
joint2_torque = st.number_input("Torque (ft-lb)", value=70)
joint2_k_factor = st.number_input("k-factor", value=0.17)

if st.button("Run Analysis"):
    joint1 = {
        'diameter': joint1_diameter,
        'tpi': joint1_tpi,
        'quantity': joint1_quantity,
        'material_strength': joint1_material_strength,
        'torque': joint1_torque,
        'k_factor': joint1_k_factor
    }
    
    joint2 = {
        'diameter': joint2_diameter,
        'tpi': joint2_tpi,
        'quantity': joint2_quantity,
        'material_strength': joint2_material_strength,
        'torque': joint2_torque,
        'k_factor': joint2_k_factor
    }
    
    results = bolted_joint_analysis(joint1, joint2)
    
    st.header("Results")
    st.write(f"Preload for Joint 1: {results['preload1']} lbf")
    st.write(f"Preload for Joint 2: {results['preload2']} lbf")
    st.write(f"Total Clamping Force for Joint 1: {results['clamping_force1']} lbf")
    st.write(f"Total Clamping Force for Joint 2: {results['clamping_force2']} lbf")
    st.write(f"Equivalent Strength for Joint 1: {results['equivalent_strength1']} lbf·psi")
    st.write(f"Equivalent Strength for Joint 2: {results['equivalent_strength2']} lbf·psi")
    st.write(f"Strength Ratio: {results['strength_ratio']}%")
    st.write(f"Result: {results['result']}")
