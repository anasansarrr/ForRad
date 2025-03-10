import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

def generate_random_numbers(ranges, num_rows, use_whole_numbers):
    """Generates a DataFrame with random numbers for given ranges."""
    data = {}
    for i, (low, high) in enumerate(ranges):
        column_name = f"Column {i+1} (Range {low}-{high})"
        if use_whole_numbers:
            # For whole numbers, we use randint which includes both endpoints
            data[column_name] = np.random.randint(int(low), int(high) + 1, num_rows)
        else:
            # For decimal numbers, we use uniform distribution
            data[column_name] = np.random.uniform(low, high, num_rows)
    df = pd.DataFrame(data)
    df.index.name = "Index"
    return df

st.title("Enhanced Random Number Generator")

# User input for number of rows to generate
num_rows = st.number_input("How many numbers do you want to generate per column?", 
                          min_value=1, max_value=1000, value=100, step=1)

# Option to choose between whole numbers or decimal numbers
use_whole_numbers = st.checkbox("Generate whole numbers (integers) instead of decimal numbers", value=False)

# User input for ranges
ranges = []
num_ranges = st.number_input("How many ranges do you want to input?", min_value=1, max_value=25, value=1, step=1)

for i in range(num_ranges):
    col1, col2 = st.columns(2)
    with col1:
        low = st.number_input(f"Lower bound for Column {i+1}", value=0.0, key=f"low_{i}")
    with col2:
        high = st.number_input(f"Upper bound for Column {i+1}", value=100.0, key=f"high_{i}")
    if low < high:
        ranges.append((low, high))
    else:
        st.warning(f"Ensure that lower bound is less than upper bound for Column {i+1}")

df = None
if st.button("Generate Random Numbers"):
    if ranges:
        df = generate_random_numbers(ranges, num_rows, use_whole_numbers)
        st.session_state.df = df  # Store in session state
        st.write("Generated Data:", df)

# Ensure df persists
if 'df' in st.session_state:
    df = st.session_state.df

    # User-defined column operations
    st.subheader("Create a New Column with Operations")
    
    # Select columns to operate on
    selected_cols = st.multiselect("Select columns to perform operation on", df.columns)

    # **Dropdown should always be visible**
    operation = st.selectbox("Select operation", ["Add", "Subtract", "Multiply", "Divide"], key="operation")

    # Only perform operation if at least 2 columns are selected
    if st.button("Perform Operation") and len(selected_cols) > 1:
        new_col_name = f"{' '.join(selected_cols)} {operation}"
        
        if operation == "Add":
            df[new_col_name] = df[selected_cols].sum(axis=1)
        elif operation == "Subtract":
            df[new_col_name] = df[selected_cols[0]] - df[selected_cols[1]]
        elif operation == "Multiply":
            df[new_col_name] = df[selected_cols].prod(axis=1)
        elif operation == "Divide":
            df[new_col_name] = df[selected_cols[0]] / df[selected_cols[1]].replace(0, np.nan)  # Avoid division by zero

        st.session_state.df = df  # Update session state
        st.write("Updated Data with New Column:", df)

    # Save to Excel using in-memory storage
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=True)
    output.seek(0)

    # Provide download button
    st.download_button("Download Excel File", output, file_name="random_numbers.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")