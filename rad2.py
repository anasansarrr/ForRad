import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO  # For handling in-memory file operations

def generate_random_numbers(ranges):
    data = {}
    for i, (low, high) in enumerate(ranges):
        column_name = f"Column {i+1} (Range {low}-{high})"
        data[column_name] = np.random.uniform(low, high, 80)
    df = pd.DataFrame(data)
    df.index.name = "Index"
    return df

st.title("Enhanced Random Number Generator")

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
        df = generate_random_numbers(ranges)
        st.session_state.df = df
        st.write("Generated Data:", df)

if 'df' in st.session_state:
    df = st.session_state.df
    
    # Optional: User-defined column operations
    st.subheader("Create a New Column with Operations (Optional)")
    selected_cols = st.multiselect("Select columns to perform operation on (leave empty if not needed)", df.columns)
    
    if selected_cols and len(selected_cols) > 1:
        operation = st.selectbox("Select operation", ["Add", "Subtract", "Multiply", "Divide"])
        new_col_name = f"{' '.join(selected_cols)} {operation}"
        
        if operation == "Add":
            df[new_col_name] = df[selected_cols].sum(axis=1)
        elif operation == "Subtract":
            df[new_col_name] = df[selected_cols[0]] - df[selected_cols[1]]
        elif operation == "Multiply":
            df[new_col_name] = df[selected_cols].prod(axis=1)
        elif operation == "Divide":
            try:
                df[new_col_name] = df[selected_cols[0]] / df[selected_cols[1]]
            except ZeroDivisionError:
                st.error("Division by zero encountered in operation.")
        
        st.write("Updated Data with New Column:", df)

    # Save to an in-memory buffer instead of writing to disk
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True)
    output.seek(0)  # Reset buffer position to start
    
    # Download button
    st.download_button(
        label="Download Excel File",
        data=output,
        file_name="random_numbers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
