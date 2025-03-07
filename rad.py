import streamlit as st
import pandas as pd
import numpy as np

def generate_random_numbers(ranges):
    data = {}
    for i, (low, high) in enumerate(ranges):
        column_name = f"Range {low}-{high}"
        data[column_name] = np.random.uniform(low, high, 102)
    return pd.DataFrame(data)

# Streamlit UI
st.title("Random Number Generator for Multiple Ranges")

# Allow user to input multiple ranges
ranges = []
num_ranges = st.number_input("How many ranges do you want to input?", min_value=1, max_value=25, value=1, step=1)

for i in range(num_ranges):
    col1, col2 = st.columns(2)
    with col1:
        low = st.number_input(f"Lower bound for Range {i+1}", value=0.0, key=f"low_{i}")
    with col2:
        high = st.number_input(f"Upper bound for Range {i+1}", value=100.0, key=f"high_{i}")
    if low < high:
        ranges.append((low, high))
    else:
        st.warning(f"Ensure that lower bound is less than upper bound for Range {i+1}")

if st.button("Generate Random Numbers"):
    if ranges:
        df = generate_random_numbers(ranges)
        st.write("Generated Data:", df)
        
        # Save to Excel
        excel_filename = "random_numbers.xlsx"
        df.to_excel(excel_filename, index=False)
        
        # Provide download link
        with open(excel_filename, "rb") as f:
            st.download_button("Download Excel File", f, file_name=excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
