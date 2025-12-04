import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# DATA LOADING FUNCTIONS
# -----------------------------

#data_url = 'https://docs.google.com/spreadsheets/d/1fTpJACr1Ay6DEIgFxjFZF8LgEPiwwAFY/edit?usp=sharing&ouid=103457517634340619188&rtpof=true&sd=true'
data_url = "data_files/data.xlsx"

def load_file(path):
    # Make URL pandas-friendly
    # modified_url = data_url.replace('/edit?usp=sharing', '/export?format=xlsx')

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

    if "Copyright" not in data:
        st.warning("No 'Copyright' sheet found.")
        return

    # Build the metadata text
    lines = [row[0] for row in data["Copyright"].dropna().values.tolist()]
    text = "\n".join(lines)

    st.text(text)


def tab_dictionary(data):
    """Show the cleaned data dictionary."""
    st.header("📘 Data Dictionary")

    if "Data Dictionary" not in data:
        st.warning("No 'Data Dictionary' sheet found.")
        return

    headers = data['Data Dictionary'].iloc[1, :].values.tolist()
    df = data['Data Dictionary'].iloc[2:, :]
    df.columns = headers
    df.reset_index(drop=True, inplace=True)

    st.dataframe(df, use_container_width=True)


def tab_data(data):
    """Show the Switchbacks sheet."""
    st.header("📊 Data Preview")

    if "Switchbacks" not in data:
        st.warning("No 'Switchbacks' sheet found.")
        return

    st.subheader("Switchbacks Sheet")
    st.dataframe(data["Switchbacks"], use_container_width=True)

    # Placeholder for visuals later
    st.info("Visualizations will be added here in the next step.")


# -----------------------------
# MAIN APP LAYOUT
# -----------------------------

st.title("📊 HBR - UBER Case Study Dashboard")
st.markdown("A simple dashboard built from a multi-sheet Excel file.")

tab1, tab2, tab3 = st.tabs(["Metadata", "Dictionary", "Data"])

with tab1:
    tab_metadata(data)

with tab2:
    tab_dictionary(data)

with tab3:
    tab_data(data)
