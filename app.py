import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Dishaba Mine Signage Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("Dishaba Mine - Signage Production Tracker")
st.write("Enter the finished quantities in the table below. The remaining counts will update automatically.")

# Function to parse and standardize all sheets from Dishaba Excel
@st.cache_data
def load_all_sheets(uploaded_file):
    file_path = uploaded_file if uploaded_file is not None else "Dishaba Mine signages (002).xlsx"
    
    try:
        xls = pd.ExcelFile(file_path)
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return {}

    parsed_sheets = {}

    for sheet in xls.sheet_names:
        raw_df = pd.read_excel(xls, sheet_name=sheet)
        
        # Standardize column header identification across non-standard rows
        records = []
        current_area = sheet

        for idx, row in raw_df.iterrows():
            row_vals = [str(val).strip() for val in row.values if pd.notna(val)]
            
            # Skip title / header rows
            if not row_vals or "DESCRIPTION" in row_vals or "Reflective" in row_vals[0]:
                continue
                
            # Check for section area markers (e.g. 10 Level, Bank area, etc.)
            val0 = str(row.iloc[0]).strip()
            if pd.notna(row.iloc[0]) and val0 not in ["nan", ""] and len(row_vals) <= 2:
                current_area = val0
            
            # Extract quantity and description
            desc = None
            qty = None
            
            for cell in row.values:
                if pd.notna(cell):
                    cell_str = str(cell).strip()
                    if cell_str.isdigit() and qty is None:
                        qty = int(cell_str)
                    elif len(cell_str) > 2 and cell_str not in ["Surface", "Underground", "nan"] and desc is None:
                        desc = cell_str
            
            if desc and qty is not None:
                records.append({
                    "Area": current_area,
                    "DESCRIPTION": desc,
                    "Total Qty": qty,
                    "Print Done": 0,
                    "Frame Done": 0
                })
        
        if records:
            df_parsed = pd.DataFrame(records)
            df_parsed["Print Left"] = df_parsed["Total Qty"] - df_parsed["Print Done"]
            df_parsed["Frame Left"] = df_parsed["Total Qty"] - df_parsed["Frame Done"]
            parsed_sheets[sheet] = df_parsed

    return parsed_sheets

# File Uploader
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls"])

sheets_data = load_all_sheets(uploaded_file)

if not sheets_data:
    st.warning("No valid signage data found in the Excel file.")
    st.stop()

# Sheet / View Selection
options = ["All Shafts Combined"] + list(sheets_data.keys())
selected_tab = st.sidebar.selectbox("Select Shaft / View", options)

# Get current table dataset
if selected_tab == "All Shafts Combined":
    current_df = pd.concat(sheets_data.values(), ignore_index=True)
else:
    current_df = sheets_data[selected_tab]

# Ensure integer types for math
for col in ["Total Qty", "Print Done", "Frame Done"]:
    current_df[col] = pd.to_numeric(current_df[col], errors='coerce').fillna(0).astype(int)

# Dynamic Table Editor
edited_df = st.data_editor(
    current_df,
    column_config={
        "Area": st.column_config.TextColumn("Area", disabled=True),
        "DESCRIPTION": st.column_config.TextColumn("Description", disabled=True),
        "Total Qty": st.column_config.NumberColumn("Total Qty", disabled=True),
        "Print Done": st.column_config.NumberColumn("Print Done", min_value=0),
        "Print Left": st.column_config.NumberColumn("Print Left", disabled=True),
        "Frame Done": st.column_config.NumberColumn("Frame Done", min_value=0),
        "Frame Left": st.column_config.NumberColumn("Frame Left", disabled=True),
    },
    use_container_width=True,
    hide_index=True,
    key=f"editor_{selected_tab}"
)

# Recalculate remaining quantities dynamically on edit
edited_df["Print Left"] = edited_df["Total Qty"] - edited_df["Print Done"]
edited_df["Frame Left"] = edited_df["Total Qty"] - edited_df["Frame Done"]

# Summary Counters
st.markdown("---")
st.subheader("Production Progress Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Items to Manufacture", f"{int(edited_df['Total Qty'].sum()):,}")

with c2:
    total_print_left = int(edited_df["Print Left"].sum())
    st.metric("Blue (Print) Left", f"{total_print_left:,}")

with c3:
    total_frame_left = int(edited_df["Frame Left"].sum())
    st.metric("Green (Frame) Left", f"{total_frame_left:,}")
