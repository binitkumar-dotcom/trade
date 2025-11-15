import streamlit as st
import pandas as pd

# Title of the app
st.title("Restore Log Viewer and Exporter")

# Load the restore log CSV file
log_file = "restored_jobs_log.csv"
try:
    df = pd.read_csv(log_file, parse_dates=["Restore Timestamp"])
except FileNotFoundError:
    st.error(f"Log file '{log_file}' not found.")
    st.stop()
except Exception as e:
    st.error(f"Error loading log file: {e}")
    st.stop()

# Ensure Restore Timestamp is datetime
df["Restore Timestamp"] = pd.to_datetime(df["Restore Timestamp"], errors='coerce')

# Check if the dataframe is empty or has invalid timestamps
if df["Restore Timestamp"].isna().all():
    st.warning("No valid restore timestamps found in the log.")
    st.stop()

# Date range filter
st.subheader("Filter by Restore Date")
min_date = df["Restore Timestamp"].min().date()
max_date = df["Restore Timestamp"].max().date()
start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

# Filter the dataframe
filtered_df = df[(df["Restore Timestamp"].dt.date >= start_date) & (df["Restore Timestamp"].dt.date <= end_date)]

# Display filtered data
st.subheader("Filtered Restore Log")
st.dataframe(filtered_df)

# Export filtered data to CSV
st.subheader("Export Filtered Log")
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Filtered Log as CSV",
    data=csv_data,
    file_name="filtered_restored_jobs_log.csv",
    mime="text/csv"
)
