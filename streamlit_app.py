import os
import requests
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

try:
    API_URL = st.secrets["API_URL"]
except st.errors.StreamlitSecretNotFoundError:
    API_URL = os.getenv(
        "API_URL",
        "http://127.0.0.1:8000"
    )


st.set_page_config(
    page_title="Smart Parking Management",
    page_icon="🚗",
    layout="wide",
)


# ============================================================
# API FUNCTIONS
# ============================================================

def get_dashboard():

    try:
        response = requests.get(
            f"{API_URL}/dashboard",
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException:
        pass

    return None


def get_vehicles():

    try:
        response = requests.get(
            f"{API_URL}/vehicles",
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException:
        pass

    return []


def get_available_slots():

    try:
        response = requests.get(
            f"{API_URL}/slots/available",
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException:
        pass

    return []


def get_history():

    try:
        response = requests.get(
            f"{API_URL}/history",
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException:
        pass

    return []


def park_vehicle(registration_number, vehicle_type):

    try:
        response = requests.post(
            f"{API_URL}/vehicles/park",
            json={
                "registration_number": registration_number,
                "vehicle_type": vehicle_type,
            },
            timeout=10
        )

        return response

    except requests.exceptions.RequestException:
        return None


def exit_vehicle(registration_number):

    try:
        response = requests.post(
            f"{API_URL}/vehicles/exit",
            json={
                "registration_number": registration_number
            },
            timeout=10
        )

        return response

    except requests.exceptions.RequestException:
        return None


# ============================================================
# LOAD DASHBOARD
# ============================================================

dashboard = get_dashboard()

if dashboard is None:

    st.error(
        "Could not connect to the FastAPI backend."
    )

    st.code(API_URL)

    st.info(
        "Check that the FastAPI server is running "
        "and that API_URL is configured correctly."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("🚗 Smart Parking Management System")

st.caption(
    "Real-time parking management, vehicle tracking "
    "and parking analytics"
)


# ============================================================
# DASHBOARD METRICS
# ============================================================

st.subheader("Parking Overview")

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


st.divider()


# ============================================================
# REVENUE
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "💰 Total Revenue",
        f'₹{dashboard["total_revenue"]:.2f}'
    )

with col2:

    occupancy = dashboard["occupancy_rate"]

    if occupancy >= 90:

        st.warning(
            "⚠️ Parking lot is almost full."
        )

    elif occupancy >= 70:

        st.info(
            "Parking occupancy is currently high."
        )

    else:

        st.success(
            "Parking availability is healthy."
        )


st.divider()


# ============================================================
# PARK / EXIT
# ============================================================

st.subheader("Vehicle Management")

park_tab, exit_tab = st.tabs(
    ["🚗 Park Vehicle", "🚪 Exit Vehicle"]
)


# ------------------------------------------------------------
# PARK VEHICLE
# ------------------------------------------------------------

with park_tab:

    with st.form("park_vehicle_form"):

        registration_number = st.text_input(
            "Vehicle Registration Number",
            placeholder="e.g. KA01AB1234"
        )

        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["Bike", "Car", "Truck"]
        )

        submitted = st.form_submit_button(
            "Park Vehicle",
            use_container_width=True
        )

    if submitted:

        registration_number = (
            registration_number.strip().upper()
        )

        if not registration_number:

            st.error(
                "Please enter a vehicle registration number."
            )

        else:

            response = park_vehicle(
                registration_number,
                vehicle_type
            )

            if response is None:

                st.error(
                    "Could not connect to the backend."
                )

            elif response.status_code == 200:

                data = response.json()

                if data["success"]:

                    st.success(
                        data["message"]
                    )

                    st.info(
                        f'🅿️ Assigned Slot: '
                        f'{data["slot_id"]}'
                    )

                    st.rerun()

                else:

                    st.error(
                        data["message"]
                    )

            else:

                st.error(
                    f"Failed to park vehicle "
                    f"(HTTP {response.status_code})."
                )


# ------------------------------------------------------------
# EXIT VEHICLE
# ------------------------------------------------------------

with exit_tab:

    with st.form("exit_vehicle_form"):

        exit_registration = st.text_input(
            "Vehicle Registration Number",
            placeholder="e.g. KA01AB1234"
        )

        exit_submitted = st.form_submit_button(
            "Exit Vehicle",
            use_container_width=True
        )

    if exit_submitted:

        exit_registration = (
            exit_registration.strip().upper()
        )

        if not exit_registration:

            st.error(
                "Please enter a vehicle registration number."
            )

        else:

            response = exit_vehicle(
                exit_registration
            )

            if response is None:

                st.error(
                    "Could not connect to the backend."
                )

            elif response.status_code == 200:

                data = response.json()

                if data["success"]:

                    st.success(
                        data["message"]
                    )

                    st.metric(
                        "Parking Fee",
                        f'₹{data["fee"]:.2f}'
                    )

                    st.rerun()

                else:

                    st.error(
                        data["message"]
                    )

            else:

                st.error(
                    f"Failed to exit vehicle "
                    f"(HTTP {response.status_code})."
                )


st.divider()


# ============================================================
# PARKING LOT VISUALIZATION
# ============================================================

st.subheader("🅿️ Parking Lot")

available_slots = get_available_slots()
vehicles = get_vehicles()


# Create occupied slot lookup

occupied_slots = {}

for vehicle in vehicles:

    if isinstance(vehicle, dict):

        slot_id = (
            vehicle.get("slot_id")
            or vehicle.get("slot")
        )

        if slot_id is not None:

            occupied_slots[int(slot_id)] = vehicle


# Create available slot lookup

available_slot_ids = set()

for slot in available_slots:

    if isinstance(slot, dict):

        slot_id = (
            slot.get("slot_id")
            or slot.get("id")
        )

        if slot_id is not None:

            available_slot_ids.add(
                int(slot_id)
            )

    elif isinstance(slot, int):

        available_slot_ids.add(slot)


total_slots = dashboard["total_slots"]


# Legend

legend_col1, legend_col2 = st.columns(2)

with legend_col1:

    st.success("🟩 Available")

with legend_col2:

    st.error("🟥 Occupied")


# Parking grid

columns_per_row = 10

for start in range(
    1,
    total_slots + 1,
    columns_per_row
):

    columns = st.columns(
        columns_per_row
    )

    for index, slot_id in enumerate(
        range(
            start,
            min(
                start + columns_per_row,
                total_slots + 1
            )
        )
    ):

        with columns[index]:

            if slot_id in occupied_slots:

                vehicle = occupied_slots[
                    slot_id
                ]

                registration = vehicle.get(
                    "registration_number",
                    "Occupied"
                )

                st.error(
                    f"🟥 **{slot_id}**\n\n"
                    f"{registration}"
                )

            else:

                st.success(
                    f"🟩 **{slot_id}**"
                )


st.divider()


# ============================================================
# CURRENTLY PARKED VEHICLES
# ============================================================

st.subheader("🚙 Currently Parked Vehicles")

vehicles = get_vehicles()

if not vehicles:

    st.info(
        "No vehicles are currently parked."
    )

else:

    vehicles_df = pd.DataFrame(
        vehicles
    )

    st.dataframe(
        vehicles_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# AVAILABLE SLOTS
# ============================================================

st.subheader("🟢 Available Parking Slots")

available_slots = get_available_slots()

if not available_slots:

    st.warning(
        "No parking slots are currently available."
    )

else:

    available_df = pd.DataFrame(
        available_slots
    )

    st.dataframe(
        available_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# PARKING HISTORY
# ============================================================

st.subheader("📜 Parking History")

history = get_history()

if not history:

    st.info(
        "No parking history available."
    )

else:

    history_df = pd.DataFrame(
        history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# BASIC ANALYTICS
# ============================================================

st.subheader("📊 Parking Analytics")

if history:

    history_df = pd.DataFrame(
        history
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Vehicle type distribution
    # --------------------------------------------------------

    with col1:

        type_column = None

        for column in [
            "vehicle_type",
            "type"
        ]:

            if column in history_df.columns:

                type_column = column
                break

        if type_column:

            st.markdown(
                "#### Vehicles by Type"
            )

            type_counts = (
                history_df[type_column]
                .value_counts()
            )

            st.bar_chart(
                type_counts
            )

        else:

            st.info(
                "Vehicle type data is not available."
            )


    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    with col2:

        fee_column = None
        exit_time_column = None

        for column in [
            "fee",
            "parking_fee"
        ]:

            if column in history_df.columns:

                fee_column = column
                break

        for column in [
            "exit_time",
            "exited_at",
            "exit_datetime"
        ]:

            if column in history_df.columns:

                exit_time_column = column
                break

        if fee_column and exit_time_column:

            st.markdown(
                "#### Revenue Over Time"
            )

            revenue_df = history_df[
                [exit_time_column, fee_column]
            ].copy()

            revenue_df[exit_time_column] = pd.to_datetime(
                revenue_df[exit_time_column],
                errors="coerce"
            )

            revenue_df[fee_column] = pd.to_numeric(
                revenue_df[fee_column],
                errors="coerce"
            ).fillna(0)

            revenue_df = revenue_df.dropna(
                subset=[exit_time_column]
            )

            revenue_data = (
                revenue_df
                .groupby(
                    revenue_df[exit_time_column].dt.date
                )[fee_column]
                .sum()
            )

            st.line_chart(
                revenue_data
            )

        else:

            st.info(
                "Revenue data is not available."
            )

else:

    st.info(
        "Analytics will appear once parking "
        "history is available."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Smart Parking Management System • "
    "Streamlit + FastAPI + PostgreSQL"
)