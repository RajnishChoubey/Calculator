import streamlit as st
import pandas as pd

# Initialize session state for emission factors if not already done
if 'emission_factors' not in st.session_state:
    st.session_state.emission_factors = {
        "LFO <80 CST": {
            "LCV_MJ_g": 0.041, "GHG_WtW_gCO2e_MJ": 91.39, "CO2_TtW_gCO2e_MJ": 76.85,
        },
        "LFO> 80 CST": {
            "LCV_MJ_g": 0.0405, "GHG_WtW_gCO2e_MJ": 91.74, "CO2_TtW_gCO2e_MJ": 76.89,
        },
        "HFO": {
            "LCV_MJ_g": 0.0405, "GHG_WtW_gCO2e_MJ": 91.74, "CO2_TtW_gCO2e_MJ": 76.89,
        },
        "MDO/MGO": {
            "LCV_MJ_g": 0.0427, "GHG_WtW_gCO2e_MJ": 90.77, "CO2_TtW_gCO2e_MJ": 75.08,
        },
        "LPG (P)": {
            "LCV_MJ_g": 0.046, "GHG_WtW_gCO2e_MJ": 74.21, "CO2_TtW_gCO2e_MJ": 65.22,
        },
        "LPG (B)": {
            "LCV_MJ_g": 0.046, "GHG_WtW_gCO2e_MJ": 74.86, "CO2_TtW_gCO2e_MJ": 65.87,
        },
        "LNG Otto MS": {
            "LCV_MJ_g": 0.0491, "GHG_WtW_gCO2e_MJ": 89.20, "CO2_TtW_gCO2e_MJ": 54.27,
        },
        "LNG Otto SS": {
            "LCV_MJ_g": 0.0491, "GHG_WtW_gCO2e_MJ": 82.87, "CO2_TtW_gCO2e_MJ": 55.06,
        },
        "LNG Diesel SS": {
            "LCV_MJ_g": 0.0491, "GHG_WtW_gCO2e_MJ": 76.08, "CO2_TtW_gCO2e_MJ": 55.90,
        },
        "LBSI": {
            "LCV_MJ_g": 0.0491, "GHG_WtW_gCO2e_MJ": 86.94, "CO2_TtW_gCO2e_MJ": 54.55,
        },
        "Biofuel 1": {
            "LCV_MJ_g": 0.037, "GHG_WtW_gCO2e_MJ": 16.28, "CO2_TtW_gCO2e_MJ": 76.59,
        },
        "Biofuel 2": {
            "LCV_MJ_g": 0.0, "GHG_WtW_gCO2e_MJ": 0.0, "CO2_TtW_gCO2e_MJ": 0.0,
        },
        "Biofuel 3": {
            "LCV_MJ_g": 0.0, "GHG_WtW_gCO2e_MJ": 0.0, "CO2_TtW_gCO2e_MJ": 0.0,
        }
    }

FUEL_LIST = list(st.session_state.emission_factors.keys())

def calc_energy_mt(fuel_mass_ton, lcv_mj_g):
    """Calculate energy in MJ from fuel mass and LCV"""
    return lcv_mj_g * fuel_mass_ton * 1e6

def calc_ghg_mt(total_energy_mj, ghg_ef_wtw):
    """Calculate GHG emissions in MT from energy and emission factor"""
    return total_energy_mj * ghg_ef_wtw / 1e6

def calc_co2_mt(total_energy_mj, co2_ef_ttw):
    """Calculate CO2 emissions in MT from energy and emission factor"""
    return total_energy_mj * co2_ef_ttw / 1e6

def calc_eua(co2_mt):
    """Calculate EUAs (1 EUA per 1 ton CO2)"""
    return co2_mt

# Page configuration
st.set_page_config(
    page_title="EU ETS & FuelEU Maritime Calculator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚢 EU ETS & FuelEU Maritime Emissions Calculator")

# Sidebar for Biofuel Configuration
st.sidebar.header("⚙️ Biofuel Configuration")
st.sidebar.write("Customize biofuel emission parameters:")

# Biofuel 1 Configuration
with st.sidebar.expander("🌱 Biofuel 1 Parameters", expanded=True):
    biofuel1_lcv = st.number_input(
        "LCV (MJ/g)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.emission_factors["Biofuel 1"]["LCV_MJ_g"],
        step=0.001,
        format="%.3f",
        key="bf1_lcv"
    )
    
    biofuel1_ghg_wtw = st.number_input(
        "GHG WtW (gCO2e/MJ)",
        min_value=-100.0,
        max_value=200.0,
        value=st.session_state.emission_factors["Biofuel 1"]["GHG_WtW_gCO2e_MJ"],
        step=0.01,
        format="%.2f",
        key="bf1_ghg"
    )
    
    biofuel1_co2_ttw = st.number_input(
        "CO2 TtW (gCO2e/MJ)",
        min_value=0.0,
        max_value=200.0,
        value=st.session_state.emission_factors["Biofuel 1"]["CO2_TtW_gCO2e_MJ"],
        step=0.01,
        format="%.2f",
        key="bf1_co2"
    )
    
    if st.button("🔄 Update Biofuel 1", key="update_bf1"):
        st.session_state.emission_factors["Biofuel 1"]["LCV_MJ_g"] = biofuel1_lcv
        st.session_state.emission_factors["Biofuel 1"]["GHG_WtW_gCO2e_MJ"] = biofuel1_ghg_wtw
        st.session_state.emission_factors["Biofuel 1"]["CO2_TtW_gCO2e_MJ"] = biofuel1_co2_ttw
        st.success("✅ Updated!")
        st.rerun()

# Create 3 main tabs
tab1, tab2, tab3 = st.tabs(["📋 Ship & Voyage Details", "⛽ Fuel Consumption", "📊 Results & Analysis"])

# TAB 1: Ship & Voyage Details
with tab1:
    st.header("Ship Particulars & Voyage Information")
    
    # Create two columns for ship particulars
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚢 Ship Particulars")
        vessel_name = st.text_input("Vessel Name", "Pacific Ruby")
        imo_number = st.text_input("IMO Number", "1234567")
        is_df_vessel = st.selectbox("Is Dual Fuel Vessel?", ["Yes", "No"], index=0)
        main_engine = st.selectbox('Main Engine Type', FUEL_LIST, index=6)  # Default to LNG Otto SS
        aux_engine = st.selectbox('Auxiliary Engine Type', FUEL_LIST, index=6)
        
        st.subheader("📈 GHG Parameters")
        year = st.number_input("Year", value=2025, min_value=2020, max_value=2050)
        ghg_target = st.number_input("GHG Target (gCO2e/MJ)", value=89.3368, format="%.4f")
        gwp_ch4 = st.number_input("GWP CH4", value=25)
        gwp_n2o = st.number_input("GWP N2O", value=298)
    
    with col2:
        st.subheader("🌍 Voyage Details")
        from_port = st.text_input("From Port", "Cadiz")
        from_port_code = st.text_input("From Port UNLOCODE", "")
        to_port = st.text_input("To Port", "Singapore")
        to_port_code = st.text_input("To Port UNLOCODE", "")
        voyage_no = st.text_input("Voyage No.", "202502 VNGDA-ESCAD")
        
        st.subheader("📅 Schedule & Distance")
        col2a, col2b = st.columns(2)
        with col2a:
            departure_date = st.date_input("Departure Date")
            departure_time = st.text_input("Departure Time (hh:mm)", "11:00")
        with col2b:
            arrival_date = st.date_input("Arrival Date")
            arrival_time = st.text_input("Arrival Time (hh:mm)", "10:18")
        
        distance = st.number_input("Distance (nm)", value=1873, min_value=0)
        cargo_carried = st.number_input("Cargo Carried (tonnes)", value=13612, min_value=0)
        condition = st.selectbox("Condition", ["Laden", "Ballast"])
        port_activity = st.selectbox("Port Activity", ["Loading", "Discharging", "Other"])

# TAB 2: Fuel Consumption
with tab2:
    st.header("⛽ Fuel Consumption Input")
    
    # Initialize fuel inputs in session state
    if 'fuel_inputs' not in st.session_state:
        st.session_state.fuel_inputs = {fuel: {
            "ME_Consumption_Sailing": 0.0,
            "AE_Consumption_Sailing": 0.0,
            "Other_Consumption_Sailing": 0.0,
            "ME_Consumption_Port": 0.0,
            "AE_Consumption_Port": 0.0,
            "Other_Consumption_Port": 0.0
        } for fuel in FUEL_LIST}
    
    # Group fuels into categories for better organization
    conventional_fuels = ["LFO <80 CST", "LFO> 80 CST", "HFO", "MDO/MGO"]
    gas_fuels = ["LPG (P)", "LPG (B)", "LNG Otto MS", "LNG Otto SS", "LNG Diesel SS", "LBSI"]
    biofuels = ["Biofuel 1", "Biofuel 2", "Biofuel 3"]
    
    # Create three columns for fuel categories
    fuel_col1, fuel_col2, fuel_col3 = st.columns(3)
    
    with fuel_col1:
        st.subheader("🛢️ Conventional Fuels")
        for fuel_type in conventional_fuels:
            with st.expander(f"{fuel_type}", expanded=False):
                # Show emission factors
                factors = st.session_state.emission_factors[fuel_type]
                st.info(f"**LCV:** {factors['LCV_MJ_g']:.3f} MJ/g | **GHG:** {factors['GHG_WtW_gCO2e_MJ']:.2f} gCO2e/MJ")
                
                st.write("**⛵ Sailing Consumption (tonnes)**")
                me_sailing = st.number_input("ME", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_me_sail")
                ae_sailing = st.number_input("AE", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_ae_sail")
                other_sailing = st.number_input("Other", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_other_sail")
                
                st.write("**🏭 Port Consumption (tonnes)**")
                me_port = st.number_input("ME", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_me_port")
                ae_port = st.number_input("AE", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_ae_port")
                other_port = st.number_input("Other", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_other_port")
                
                st.session_state.fuel_inputs[fuel_type] = {
                    "ME_Consumption_Sailing": me_sailing,
                    "AE_Consumption_Sailing": ae_sailing,
                    "Other_Consumption_Sailing": other_sailing,
                    "ME_Consumption_Port": me_port,
                    "AE_Consumption_Port": ae_port,
                    "Other_Consumption_Port": other_port
                }
    
    with fuel_col2:
        st.subheader("💨 Gas Fuels")
        for fuel_type in gas_fuels:
            with st.expander(f"{fuel_type}", expanded=False):
                # Show emission factors
                factors = st.session_state.emission_factors[fuel_type]
                st.info(f"**LCV:** {factors['LCV_MJ_g']:.3f} MJ/g | **GHG:** {factors['GHG_WtW_gCO2e_MJ']:.2f} gCO2e/MJ")
                
                st.write("**⛵ Sailing Consumption (tonnes)**")
                me_sailing = st.number_input("ME", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_me_sail")
                ae_sailing = st.number_input("AE", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_ae_sail")
                other_sailing = st.number_input("Other", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_other_sail")
                
                st.write("**🏭 Port Consumption (tonnes)**")
                me_port = st.number_input("ME", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_me_port")
                ae_port = st.number_input("AE", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_ae_port")
                other_port = st.number_input("Other", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_other_port")
                
                st.session_state.fuel_inputs[fuel_type] = {
                    "ME_Consumption_Sailing": me_sailing,
                    "AE_Consumption_Sailing": ae_sailing,
                    "Other_Consumption_Sailing": other_sailing,
                    "ME_Consumption_Port": me_port,
                    "AE_Consumption_Port": ae_port,
                    "Other_Consumption_Port": other_port
                }
    
    with fuel_col3:
        st.subheader("🌱 Biofuels")
        for fuel_type in biofuels:
            with st.expander(f"{fuel_type}", expanded=fuel_type == "Biofuel 1"):
                # Show emission factors
                factors = st.session_state.emission_factors[fuel_type]
                if fuel_type == "Biofuel 1":
                    st.success(f"**LCV:** {factors['LCV_MJ_g']:.3f} MJ/g | **GHG:** {factors['GHG_WtW_gCO2e_MJ']:.2f} gCO2e/MJ")
                else:
                    st.info(f"**LCV:** {factors['LCV_MJ_g']:.3f} MJ/g | **GHG:** {factors['GHG_WtW_gCO2e_MJ']:.2f} gCO2e/MJ")
                
                st.write("**⛵ Sailing Consumption (tonnes)**")
                me_sailing = st.number_input("ME", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_me_sail")
                ae_sailing = st.number_input("AE", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_ae_sail")
                other_sailing = st.number_input("Other", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_other_sail")
                
                st.write("**🏭 Port Consumption (tonnes)**")
                me_port = st.number_input("ME", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_me_port")
                ae_port = st.number_input("AE", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_ae_port")
                other_port = st.number_input("Other", min_value=0.0, value=0.0, step=0.1, key=f"{fuel_type}_other_port")
                
                st.session_state.fuel_inputs[fuel_type] = {
                    "ME_Consumption_Sailing": me_sailing,
                    "AE_Consumption_Sailing": ae_sailing,
                    "Other_Consumption_Sailing": other_sailing,
                    "ME_Consumption_Port": me_port,
                    "AE_Consumption_Port": ae_port,
                    "Other_Consumption_Port": other_port
                }

# TAB 3: Results & Analysis
with tab3:
    st.header("📊 Emissions Calculation Results")
    
    if st.button("🧮 Calculate Emissions", type="primary", use_container_width=True):
        # Perform calculations
        results = []
        total_sailing_fuel = 0
        total_port_fuel = 0
        
        for fuel, vals in st.session_state.fuel_inputs.items():
            factor = st.session_state.emission_factors[fuel]
            
            # Calculate total fuel consumption
            sailing_mass = vals["ME_Consumption_Sailing"] + vals["AE_Consumption_Sailing"] + vals["Other_Consumption_Sailing"]
            port_mass = vals["ME_Consumption_Port"] + vals["AE_Consumption_Port"] + vals["Other_Consumption_Port"]
            
            total_sailing_fuel += sailing_mass
            total_port_fuel += port_mass
            
            # Skip if no consumption
            if sailing_mass == 0 and port_mass == 0:
                continue
            
            # Calculate energy and emissions
            sailing_energy_mj = calc_energy_mt(sailing_mass, factor["LCV_MJ_g"])
            port_energy_mj = calc_energy_mt(port_mass, factor["LCV_MJ_g"])
            
            sailing_ghg_mt = calc_ghg_mt(sailing_energy_mj, factor["GHG_WtW_gCO2e_MJ"])
            port_ghg_mt = calc_ghg_mt(port_energy_mj, factor["GHG_WtW_gCO2e_MJ"])
            
            sailing_co2_mt = calc_co2_mt(sailing_energy_mj, factor["CO2_TtW_gCO2e_MJ"])
            port_co2_mt = calc_co2_mt(port_energy_mj, factor["CO2_TtW_gCO2e_MJ"])
            
            sailing_eua = calc_eua(sailing_co2_mt)
            port_eua = calc_eua(port_co2_mt)
            
            results.append({
                "Fuel Type": fuel,
                "Sailing Fuel (MT)": round(sailing_mass, 2),
                "Port Fuel (MT)": round(port_mass, 2),
                "Sailing Energy (TJ)": round(sailing_energy_mj/1e6, 4),
                "Port Energy (TJ)": round(port_energy_mj/1e6, 4),
                "Sailing GHG WtW (MT)": round(sailing_ghg_mt, 2),
                "Port GHG WtW (MT)": round(port_ghg_mt, 2),
                "Sailing CO2 TtW (MT)": round(sailing_co2_mt, 2),
                "Port CO2 TtW (MT)": round(port_co2_mt, 2),
                "Sailing EUAs": round(sailing_eua, 2),
                "Port EUAs": round(port_eua, 2)
            })
        
        if results:
            result_df = pd.DataFrame(results)
            
            # Display results in two columns
            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                st.subheader("📋 Detailed Results by Fuel Type")
                st.dataframe(result_df, use_container_width=True, hide_index=True)
            
            with result_col2:
                st.subheader("📈 Summary Totals")
                
                # Calculate totals
                totals = {
                    "Total Sailing Fuel (MT)": result_df["Sailing Fuel (MT)"].sum(),
                    "Total Port Fuel (MT)": result_df["Port Fuel (MT)"].sum(),
                    "Total Sailing Energy (TJ)": result_df["Sailing Energy (TJ)"].sum(),
                    "Total Port Energy (TJ)": result_df["Port Energy (TJ)"].sum(),
                    "Total Sailing GHG (MT)": result_df["Sailing GHG WtW (MT)"].sum(),
                    "Total Port GHG (MT)": result_df["Port GHG WtW (MT)"].sum(),
                    "Total Sailing CO2 (MT)": result_df["Sailing CO2 TtW (MT)"].sum(),
                    "Total Port CO2 (MT)": result_df["Port CO2 TtW (MT)"].sum(),
                    "Total Sailing EUAs": result_df["Sailing EUAs"].sum(),
                    "Total Port EUAs": result_df["Port EUAs"].sum(),
                    "Total EUAs (Sailing + Port)": result_df["Sailing EUAs"].sum() + result_df["Port EUAs"].sum()
                }
                
                # Display totals as metrics
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total Fuel Consumption", f"{totals['Total Sailing Fuel (MT)'] + totals['Total Port Fuel (MT)']:.1f} MT")
                    st.metric("Total Energy", f"{totals['Total Sailing Energy (TJ)'] + totals['Total Port Energy (TJ)']:.2f} TJ")
                    st.metric("Total GHG Emissions", f"{totals['Total Sailing GHG (MT)'] + totals['Total Port GHG (MT)']:.1f} MT CO2e")
                
                with col_b:
                    st.metric("Total CO2 Emissions", f"{totals['Total Sailing CO2 (MT)'] + totals['Total Port CO2 (MT)']:.1f} MT CO2")
                    st.metric("Total EUAs Required", f"{totals['Total EUAs (Sailing + Port)']:.1f}")
                    
                    # Calculate GHG intensity
                    total_energy = totals['Total Sailing Energy (TJ)'] + totals['Total Port Energy (TJ)']
                    total_ghg = totals['Total Sailing GHG (MT)'] + totals['Total Port GHG (MT)']
                    if total_energy > 0:
                        ghg_intensity = (total_ghg * 1e6) / (total_energy * 1e6)  # gCO2e/MJ
                        st.metric("GHG Intensity", f"{ghg_intensity:.2f} gCO2e/MJ")
            
            # Additional analysis
            st.subheader("📊 Compliance Analysis")
            
            analysis_col1, analysis_col2, analysis_col3 = st.columns(3)
            
            with analysis_col1:
                st.write("**🎯 FuelEU Maritime Compliance**")
                if total_energy > 0:
                    ghg_intensity = (total_ghg * 1e6) / (total_energy * 1e6)
                    compliance_gap = ghg_intensity - ghg_target
                    
                    if compliance_gap <= 0:
                        st.success(f"✅ Compliant! {abs(compliance_gap):.2f} gCO2e/MJ below target")
                    else:
                        st.error(f"❌ Non-compliant! {compliance_gap:.2f} gCO2e/MJ above target")
                        penalty_factor = compliance_gap * total_energy * 1e6 * 2400 / 1e6  # Simplified penalty calculation
                        st.write(f"💰 Estimated penalty: €{penalty_factor:.0f}")
            
            with analysis_col2:
                st.write("**🏭 EU ETS Summary**")
                st.write(f"Sailing EUAs: {totals['Total Sailing EUAs']:.1f}")
                st.write(f"Port EUAs: {totals['Total Port EUAs']:.1f}")
                st.write(f"**Total EUAs: {totals['Total EUAs (Sailing + Port)']:.1f}**")
                # Estimate cost (approximate EUA price)
                eua_cost = totals['Total EUAs (Sailing + Port)'] * 85  # €85 per EUA (approximate)
                st.write(f"💰 Estimated cost: €{eua_cost:.0f}")
            
            with analysis_col3:
                st.write("**📈 Voyage Efficiency**")
                if distance > 0:
                    fuel_efficiency = (totals['Total Sailing Fuel (MT)'] + totals['Total Port Fuel (MT)']) / distance * 1000  # kg/nm
                    st.write(f"Fuel efficiency: {fuel_efficiency:.2f} kg/nm")
                    
                    co2_efficiency = (totals['Total Sailing CO2 (MT)'] + totals['Total Port CO2 (MT)']) / distance * 1000  # kg CO2/nm
                    st.write(f"CO2 efficiency: {co2_efficiency:.2f} kg CO2/nm")
                
                if cargo_carried > 0:
                    cargo_efficiency = (totals['Total Sailing CO2 (MT)'] + totals['Total Port CO2 (MT)']) / cargo_carried * 1000  # kg CO2/tonne cargo
                    st.write(f"Cargo efficiency: {cargo_efficiency:.2f} kg CO2/tonne")
            
            # Download options
            st.subheader("💾 Download Results")
            download_col1, download_col2 = st.columns(2)
            
            with download_col1:
                csv_data = result_df.to_csv(index=False)
                st.download_button(
                    label="📄 Download Detailed Results (CSV)",
                    data=csv_data,
                    file_name=f"{vessel_name}_voyage_{voyage_no}_detailed_emissions.csv",
                    mime="text/csv"
                )
            
            with download_col2:
                # Create summary report
                summary_data = pd.DataFrame([totals]).T.reset_index()
                summary_data.columns = ['Metric', 'Value']
                summary_csv = summary_data.to_csv(index=False)
                
                st.download_button(
                    label="📊 Download Summary Report (CSV)",
                    data=summary_csv,
                    file_name=f"{vessel_name}_voyage_{voyage_no}_summary.csv",
                    mime="text/csv"
                )
        
        else:
            st.warning("⚠️ No fuel consumption data entered. Please add fuel consumption values in Tab 2.")
    
    else:
        st.info("👆 Click 'Calculate Emissions' to generate results after entering fuel consumption data in the Fuel Consumption tab.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    🚢 EU ETS & FuelEU Maritime Emissions Calculator | 
    Compliant with EU regulations for maritime emissions reporting
    </div>
    """, 
    unsafe_allow_html=True
)
