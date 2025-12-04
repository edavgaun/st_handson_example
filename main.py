import streamlit as st
import pandas as pd

from charts.tab3 import time_series, pie_chart

# -----------------------------
# DATA LOADING FUNCTIONS
# -----------------------------

data_url = "data_files/data.xlsx"

def load_file(path):
    # Load ALL sheets
    all_sheets = pd.read_excel(path, sheet_name=None)

    data = {}
    for sheet_name, df in all_sheets.items():
        data[sheet_name] = df
    return data

@st.cache_data
def get_data():
    return load_file(data_url)

data = get_data()

# -----------------------------
# STREAMLIT TAB FUNCTIONS
# -----------------------------

def tab_metadata(data):
    """Show the metadata extracted from the 'Copyright' sheet."""
    st.header("📄 Metadata")

    # Build the metadata text
    lines = [row[0] for row in data["Copyright"].dropna().values.tolist()]
    text = "\n".join(lines)

    st.text(text)


def tab_dictionary(data):
    """Show the cleaned data dictionary."""
    st.header("📘 Data Dictionary")

    headers = data['Data Dictionary'].iloc[1, :].values.tolist()
    df = data['Data Dictionary'].iloc[2:, :]
    df.columns = headers
    df.reset_index(drop=True, inplace=True)

    st.dataframe(df, use_container_width=True)


def tab_data(data):
    """Show the Switchbacks sheet."""
    st.header("📊 Data Preview")

    st.subheader("Switchbacks Sheet")

    df = data["Switchbacks"].drop(columns='city_id')

    # --- Double integer slider to select row range ---
    start, end = st.slider(
        "Select row range to display",
        min_value=0,
        max_value=len(df),
        value=(0, len(df)),
        step=1
    )

    st.dataframe(df.iloc[start:end], use_container_width=True, height=400)
    return df.iloc[start:end]


# -----------------------------
# MAIN APP LAYOUT
# -----------------------------

st.set_page_config(page_title="Switchbacks Dashboard", layout="wide")

# ---- HEADER WITH LEFT + RIGHT LOGOS ----
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://raw.githubusercontent.com/edavgaun/st_handson_example/refs/heads/main/data_files/Uber-logo.png' width='120'>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("<h1 style='text-align: center;'>📊 HBR - UBER Case Study Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>A simple dashboard built from a multi-sheet Excel file.</p>", unsafe_allow_html=True)

with col3:
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://raw.githubusercontent.com/edavgaun/st_handson_example/refs/heads/main/data_files/rice-logo.jpg' width='240'>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- Tabs ----

tab1, tab2, tab3 = st.tabs(["Metadata", "Dictionary", "Data"])

with tab1:
    tab_metadata(data)

with tab2:
    tab_dictionary(data)

with tab3:
    st.header("📊 Data and Time Series")

    # Create three columns: left for the table, center for the timeseries, right for the pie chart
    col1, col2, col3 = st.columns([1, 3, 1.5])

    with col1:
        st.subheader("Data Preview")
        # Get the data slice (tab_data returns the sliced DataFrame)
        time_data = tab_data(data)  

    with col2:
        st.subheader("Plot 1")
        # Pass the same slice to time_series
        time_series(time_data)

    with col3:
        st.subheader("Plot 2")   
        # Pass the same slice to pie_chart
        pie_chart(time_data)
