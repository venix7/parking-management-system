import os
import requests
import streamlit as st

try:
    API_URL = st.secrets["API_URL"]
except st.errors.StreamlitSecretNotFoundError:
    API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Parking Management System",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 Parking Management System")
st.caption("Parking management dashboard")

def get_dashboard():
    response = requests.get(f"{API_URL}/dashboard")

    if response.status_code == 200:
        return response.json()

    return None

dashboard = get_dashboard()

if dashboard is None:
    st.error("Could not connect to the FastAPI backend.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Slots",
        dashboard["total_slots"]
    )

with col2:
    st.metric(
        "Occupied",
        dashboard["occupied_slots"]
    )

with col3:
    st.metric(
        "Available",
        dashboard["available_slots"]
    )

with col4:
    st.metric(
        "Occupancy",
        f'{dashboard["occupancy_rate"]:.1f}%'
    )

st.metric(
    "Total Revenue",
    f'₹{dashboard["total_revenue"]:.2f}'
)

st.divider()

st.header("Park Vehicle")

with st.form("park_vehicle_form"):

    registration_number = st.text_input(
        "Vehicle Registration Number"
    )

    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["Bike", "Car", "Truck"]
    )

    submitted = st.form_submit_button(
        "Park Vehicle"
    )

if submitted:

    if not registration_number.strip():
        st.error("Please enter a vehicle registration number.")

    else:

        payload = {
            "registration_number": registration_number,
            "vehicle_type": vehicle_type,
        }

        response = requests.post(
            f"{API_URL}/vehicles/park",
            json=payload,
        )

        if response.status_code == 200:

            data = response.json()

            if data["success"]:
                st.success(data["message"])
                st.info(
                    f'Assigned Slot: {data["slot_id"]}'
                )

                st.rerun()

            else:
                st.error(data["message"])

        else:
            st.error("Failed to park vehicle.")

st.divider()

st.header("Exit Vehicle")

with st.form("exit_vehicle_form"):

    exit_registration = st.text_input(
        "Vehicle Registration Number",
        key="exit_vehicle"
    )

    exit_submitted = st.form_submit_button(
        "Exit Vehicle"
    )

if exit_submitted:

    if not exit_registration.strip():
        st.error(
            "Please enter a vehicle registration number."
        )

    else:

        payload = {
            "registration_number": exit_registration
        }

        response = requests.post(
            f"{API_URL}/vehicles/exit",
            json=payload,
        )

        if response.status_code == 200:

            data = response.json()

            if data["success"]:
                st.success(data["message"])

                st.info(
                    f'Parking Fee: ₹{data["fee"]:.2f}'
                )

                st.rerun()

            else:
                st.error(data["message"])

        else:
            st.error("Failed to exit vehicle.")

st.divider()

st.header("Currently Parked Vehicles")

def get_vehicles():

    response = requests.get(
        f"{API_URL}/vehicles"
    )

    if response.status_code == 200:
        return response.json()

    return []

vehicles = get_vehicles()

if not vehicles:

    st.info("No vehicles are currently parked.")

else:

    st.dataframe(
        vehicles,
        use_container_width=True,
    )

st.divider()

st.header("Available Parking Slots")

def get_available_slots():

    response = requests.get(
        f"{API_URL}/slots/available"
    )

    if response.status_code == 200:
        return response.json()

    return []

available_slots = get_available_slots()

if available_slots:

    st.dataframe(
        available_slots,
        use_container_width=True,
    )

else:

    st.warning("No parking slots are currently available.")

st.divider()

st.header("Parking History")

def get_history():

    response = requests.get(
        f"{API_URL}/history"
    )

    if response.status_code == 200:
        return response.json()

    return []

history = get_history()

if history:

    st.dataframe(
        history,
        use_container_width=True,
    )

else:

    st.info("No parking history available.")