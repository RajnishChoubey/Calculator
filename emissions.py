import streamlit as st
from datetime import datetime
import json
import csv
import io

# Field configuration
fuel_types = [
    "LFO", "HFO", "MGO",
    "LPG(P)", "LPG(B)", "LNG Otto MS", "LNG Otto SS",
    "LNG Diesel SS", "LNG LBSI", "BioFuel 1", "BioFuel 2", "BioFuel 3"
]
engine_types = ["ME", "AE", "Others", "Off-hire"]

def validate_imo_number(imo: str) -> bool:
    return imo.isdigit() and len(imo) == 7

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except:
        return False

def validate_time(time_str: str) -> bool:
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except:
        return False

def validate_percentage(value: float) -> bool:
    return value in [0, 50, 100]

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def download_csv(data: dict):
    # Flatten for CSV
    flat = flatten_dict(data)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Field', 'Value'])
    for k, v in flat.items():
        writer.writerow([k, v])
    return output.getvalue()

# Main form
st.title("EU ETS and FuelEU Maritime Calculator")
st.write("Enter all voyage details, emission data, and fuel measurements:")

with st.form("voyage_form"):
    st.header("Basic Voyage Information")
    imo_number = st.text_input("IMO No.")
    vessel = st.text_input("Vessel")
    application_year = st.text_input("Application Year")
    emission_statement_number = st.text_input("Emission Statement Number")
    voyage_number = st.text_input("Voyage no.")
    condition = st.selectbox("Condition (Laden/Ballast)", ["Laden", "Ballast"])

    st.header("Route Information")
    from_port = st.text_input("From (port)")
    from_port_eu = st.selectbox("From (port) EU/Non-EU", ["EU", "Non-EU"])
    to_port = st.text_input("To (Port)")
    to_port_eu = st.selectbox("To (port) EU/Non-EU", ["EU", "Non-EU"])
    eu_ets_pct = st.selectbox("Applicable EU ETS Voyage Type %", [0,50,100])
    fueleu_pct = st.selectbox("Applicable FuelEU Voyage Type %", [0,50,100])

    st.header("Sailing Schedule")
    departure_date = st.text_input("Departure Date from last berth/(anchor for STS)  (UTC)\n(dd/mm/yyyy)")
    departure_time = st.text_input("Departure Time from last berth/(anchor for STS)  (UTC)\n(hh:mm)")
    arrival_date = st.text_input("Arrival Date at first berth/ (anchor for STS) (UTC)\n(dd/mm/yyyy)")
    arrival_time = st.text_input("Arrival time at first berth/ (anchor for STS) (UTC)\n(hh:mm)")
    distance_nm = st.number_input("Distance (Nm)", min_value=0.0, format="%.2f")

    st.header("Sailing Fuel Consumption")
    sailing_fuel = {}
    for fuel in fuel_types:
        with st.expander(f"Sailing Fuel: {fuel}"):
            fuel_data = {}
            for engine in engine_types:
                val = st.number_input(f"{engine} {fuel} Sailing (MT)", min_value=0.0, value=0.0, format="%.2f",
                                    key=f"{fuel}_sailing_{engine}")
                fuel_data[engine] = val
            sailing_fuel[fuel] = fuel_data

    st.header("Port Information")
    arrival_port = st.text_input("Arrival port")
    port_activity = st.selectbox("Port Activity", ["Load", "Discharge", "Other"])
    arrival_port_eu = st.selectbox("Arrival Port EU or Non-EU?", ["EU", "Non-EU"])
    port_arrival_date = st.text_input("Arrival Date at first berth/(anchor for STS) (UTC)\n(dd/mm/yyyy)")
    port_arrival_time = st.text_input("Arrival time at first berth/(anchor for STS) (UTC)\n(hh:mm)")
    port_departure_date = st.text_input("Departure Date from last berth/(anchor for STS)  (UTC)\n(dd/mm/yyyy)")
    port_departure_time = st.text_input("Departure time from last berth/(anchor for STS)  (UTC)\n(hh:mm)")
    port_limits = st.selectbox("Within port limits or outside port limits", ["Within port limits","Outside port limits"])
    total_stay_hours = st.number_input("Total Stay (hrs)", min_value=0.0, format="%.2f")

    st.header("Port Fuel Consumption")
    port_fuel = {}
    for fuel in fuel_types:
        with st.expander(f"Port Fuel: {fuel}"):
            fuel_data = {}
            for engine in engine_types:
                val = st.number_input(f"{engine} {fuel} Port (MT)", min_value=0.0, value=0.0, format="%.2f",
                                    key=f"{fuel}_port_{engine}")
                fuel_data[engine] = val
            port_fuel[fuel] = fuel_data

    submitted = st.form_submit_button("Submit & Review")

if submitted:
    errors = []
    if not validate_imo_number(imo_number):
        errors.append("IMO No. must be exactly 7 digits.")
    if departure_date and not validate_date(departure_date):
        errors.append("Departure date format must be dd/mm/yyyy.")
    if arrival_date and not validate_date(arrival_date):
        errors.append("Arrival date format must be dd/mm/yyyy.")
    if departure_time and not validate_time(departure_time):
        errors.append("Departure time format must be hh:mm.")
    if arrival_time and not validate_time(arrival_time):
        errors.append("Arrival time format must be hh:mm.")

    if errors:
        st.error("Please correct these errors:")
        for err in errors:
            st.write(f"- {err}")
    else:
        voyage_data = {
            "imo_number": imo_number,
            "vessel": vessel,
            "application_year": application_year,
            "emission_statement_number": emission_statement_number,
            "voyage_number": voyage_number,
            "condition": condition,
            "from_port": from_port,
            "from_port_eu": from_port_eu,
            "to_port": to_port,
            "to_port_eu": to_port_eu,
            "eu_ets_percentage": eu_ets_pct,
            "fueleu_percentage": fueleu_pct,
            "departure_date": departure_date,
            "departure_time": departure_time,
            "arrival_date": arrival_date,
            "arrival_time": arrival_time,
            "distance_nm": distance_nm,
            "sailing_fuel": sailing_fuel,
            "arrival_port": arrival_port,
            "port_activity": port_activity,
            "arrival_port_eu": arrival_port_eu,
            "port_arrival_date": port_arrival_date,
            "port_arrival_time": port_arrival_time,
            "port_departure_date": port_departure_date,
            "port_departure_time": port_departure_time,
            "port_limits": port_limits,
            "total_stay_hours": total_stay_hours,
            "port_fuel": port_fuel
        }

        st.success("All data validated and captured!")

        st.header("Summary")
        st.json(voyage_data)

        # Download Options
        st.download_button(
            label="Download JSON",
            data=json.dumps(voyage_data, indent=2),
            file_name=f"voyage_{voyage_number or 'unknown'}.json",
            mime="application/json"
        )

        st.download_button(
            label="Download CSV",
            data=download_csv(voyage_data),
            file_name=f"voyage_{voyage_number or 'unknown'}.csv",
            mime="text/csv"
        )
