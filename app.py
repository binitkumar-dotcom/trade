
import streamlit as st
import os
import csv
import pandas as pd
from datetime import datetime

# File name
file_name = "restored_jobs_log.csv"

# Ensure file exists and has headers
if not os.path.isfile(file_name) or os.path.getsize(file_name) == 0:
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["job_id", "status", "timestamp"])  # Add headers

# Load data safely
def load_data():
    return pd.read_csv(file_name)

# Append new job entry
def log_job(job_id, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([job_id, status, timestamp])

# Streamlit UI
st.title("Restored Jobs Log")

# Display current log
st.subheader("Current Jobs Log")
data = load_data()
st.dataframe(data)

# Download button
st.download_button(
    label="📥 Download CSV",
    data=data.to_csv(index=False),
    file_name=file_name,
    mime="text/csv"
)

# Add new job entry
st.subheader("Add New Job Entry")
job_id = st.text_input("Job ID")
status = st.selectbox("Status", ["restored", "failed", "pending"])

if st.button("Log Job"):
    if job_id.strip() == "":
        st.error("Job ID cannot be empty!")
    else:
        log_job(job_id, status)
        st.success(f"Job '{job_id}' logged successfully!")
        st.experimental_rerun()
