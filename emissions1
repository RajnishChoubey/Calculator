import streamlit as st
import pandas as pd

# Add emission factors (from your spreadsheet)
EMISSION_FACTORS = {
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
    }
}

FUEL_LIST = list(EMISSION_FACTORS.keys())

def calc_energy_mt(fuel_mass_ton, lcv_mj_g):
    # 1 ton = 1e6 g, so MJ = lcv * mass(ton) * 1e6
    return lcv_mj_g * fuel_mass_ton * 1e6 / 1e6  # MJ, convert to TJ below when needed

def calc_ghg_mt(total_energy_mj, ghg_ef_wtw):
    # GHG = MJ * gCO2e/MJ = gCO2e, convert to MT (divide by 1e6)
    return total_energy_mj * ghg_ef_wtw / 1e6

def calc_co2_mt(total_energy_mj, co2_ef_ttw):
    # CO2 = MJ * gCO2/MJ = gCO2, convert to MT (divide by 1e6)
    return total_energy_mj * co2_ef_ttw / 1e6

def calc_eua(co2_mt):
    # EUA = 1 EUA per 1 ton CO2
    return co2_mt

st.title("EU ETS & FuelEU Maritime Emissions Calculator")

st.header("Ship & Voyage Particulars")
vessel_name = st.text_input("Vessel Name", "Pacific Ruby")
imo_number = st.text_input("IMO Number", "1234567")
main_engine = st.selectbox('Main Engine Type', FUEL_LIST)
aux_engine = st.selectbox('Aux Engine Type', FUEL_LIST)
from_port = st.text_input("From Port", "Cadiz")
to_port = st.text_input("To Port", "Singapore")
voyage_no = st.text_input("Voyage No.", "202502 VNGDA-ESCAD")
distance = st.number_input("Distance (nm)", value=1873)
departure_date = st.date_input("Departure Date")
arrival_date = st.date_input("Arrival Date")
departure_time = st.text_input("Departure Time (hh:mm)", "11:00")
arrival_time = st.text_input("Arrival Time (hh:mm)", "10:18")
cargo_carried = st.number_input("Cargo Carried (tonnes)", value=13612)
condition = st.selectbox("Condition", ["Laden", "Ballast"])

st.header("Fuel Consumption Inputs")
fuel_inputs = {}
for fuel_type in FUEL_LIST:
    with st.expander(f"Fuel: {fuel_type}"):
        me_sailing = st.number_input(f"{fuel_type} ME Consumption Sailing (ton)", min_value=0.0, value=0.0, step=0.1)
        ae_sailing = st.number_input(f"{fuel_type} AE Consumption Sailing (ton)", min_value=0.0, value=0.0, step=0.1)
        me_port = st.number_input(f"{fuel_type} ME Consumption Port (ton)", min_value=0.0, value=0.0, step=0.1)
        ae_port = st.number_input(f"{fuel_type} AE Consumption Port (ton)", min_value=0.0, value=0.0, step=0.1)
        fuel_inputs[fuel_type] = {
            "ME_Consumption_Sailing": me_sailing,
            "AE_Consumption_Sailing": ae_sailing,
            "ME_Consumption_Port": me_port,
            "AE_Consumption_Port": ae_port
        }

if st.button("Calculate Emissions"):
    # Output dataframe
    results = []
    for fuel, vals in fuel_inputs.items():
        factor = EMISSION_FACTORS[fuel]
        sailing_mass = vals["ME_Consumption_Sailing"] + vals["AE_Consumption_Sailing"]
        port_mass = vals["ME_Consumption_Port"] + vals["AE_Consumption_Port"]
        sailing_energy_mj = calc_energy_mt(sailing_mass, factor["LCV_MJ_g"])
        port_energy_mj = calc_energy_mt(port_mass, factor["LCV_MJ_g"])
        sailing_ghg_mt = calc_ghg_mt(sailing_energy_mj, factor["GHG_WtW_gCO2e_MJ"])
        port_ghg_mt = calc_ghg_mt(port_energy_mj, factor["GHG_WtW_gCO2e_MJ"])
        sailing_co2_mt = calc_co2_mt(sailing_energy_mj, factor["CO2_TtW_gCO2e_MJ"])
        port_co2_mt = calc_co2_mt(port_energy_mj, factor["CO2_TtW_gCO2e_MJ"])
        sailing_eua = calc_eua(sailing_co2_mt)
        port_eua = calc_eua(port_co2_mt)
        results.append({
            "Fuel": fuel,
            "Sailing Fuel Used (ton)": sailing_mass,
            "Port Fuel Used (ton)": port_mass,
            "Sailing Energy (TJ)": sailing_energy_mj/1e6,
            "Port Energy (TJ)": port_energy_mj/1e6,
            "Sailing GHG WtW (MT)": sailing_ghg_mt,
            "Port GHG WtW (MT)": port_ghg_mt,
            "Sailing CO2 TtW (MT)": sailing_co2_mt,
            "Port CO2 TtW (MT)": port_co2_mt,
            "Sailing EUAs": sailing_eua,
            "Port EUAs": port_eua
        })
    result_df = pd.DataFrame(results)
    st.subheader("GHG/CO2/ETS Results (Per Fuel)")
    st.dataframe(result_df, use_container_width=True)

    st.subheader("Totals")
    total_row = {
        "Sailing Fuel Used (ton)": result_df["Sailing Fuel Used (ton)"].sum(),
        "Port Fuel Used (ton)": result_df["Port Fuel Used (ton)"].sum(),
        "Sailing Energy (TJ)": result_df["Sailing Energy (TJ)"].sum(),
        "Port Energy (TJ)": result_df["Port Energy (TJ)"].sum(),
        "Sailing GHG WtW (MT)": result_df["Sailing GHG WtW (MT)"].sum(),
        "Port GHG WtW (MT)": result_df["Port GHG WtW (MT)"].sum(),
        "Sailing CO2 TtW (MT)": result_df["Sailing CO2 TtW (MT)"].sum(),
        "Port CO2 TtW (MT)": result_df["Port CO2 TtW (MT)"].sum(),
        "Sailing EUAs": result_df["Sailing EUAs"].sum(),
        "Port EUAs": result_df["Port EUAs"].sum()
    }
    st.write(pd.DataFrame([total_row]).T.rename(columns={0:'Total'}))

    st.success("Calculation completed. Download your table below:")

    st.download_button(
        label="Download Results as CSV",
        data=result_df.to_csv(index=False),
        file_name=f"{vessel_name}_voyage_{voyage_no}_emissions.csv",
        mime="text/csv"
    )
