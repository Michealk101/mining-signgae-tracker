import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Production Progress Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("Production Progress Tracker")
st.write("Enter the finished quantities in the table below. The remaining counts will update automatically.")

# File Uploader / Default Data Load
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

@st.cache_data
def load_data(file):
    if file is not None:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    else:
        # Fallback dummy data structure matching your project
        return pd.DataFrame({
            "Area": ["2# Vertical", "2# Fridge Plant", "2# RO Plant", "2# Compressors", "2# Lamproom", "Industrial Changehouses", "2# Settling Pond", "Oxygen/Acetylene", "Chemical Store", "Oil Store"],
            "DESCRIPTION": ["Vertical Sign", "Fridge Plant Sign", "RO Plant Sign", "Compressor Sign", "Lamproom Sign", "Changehouse Sign", "Settling Pond Sign", "Safety Sign", "Chemical Storage", "Oil Storage"],
            "Total Qty": [4, 4, 4, 4, 4, 8, 3, 8, 8, 8],
            "Print Done": [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Frame Done": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        })

df = load_data(uploaded_file)

# Ensure numeric types for calculation columns
for col in ["Total Qty", "Print Done", "Frame Done"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    else:
        df[col] = 0

# Compute remaining columns dynamically initially
df["Print Left"] = df["Total Qty"] - df["Print Done"]
df["Frame Left"] = df["Total Qty"] - df["Frame Done"]

# Reorder columns to display
cols_order = [col for col in df.columns if col not in ["Print Left", "Frame Left"]]
cols_order.insert(cols_order.index("Print Done") if "Print Done" in cols_order else len(cols_order), "Print Left")
cols_order.append("Frame Left") if "Frame Left" not in cols_order else None

df_display = df[cols_order]

# Interactive Data Editor
edited_df = st.data_editor(
    df_display,
    column_config={
        "Total Qty": st.column_config.NumberColumn("Total Qty", disabled=True),
        "Print Done": st.column_config.NumberColumn("Print Done", min_value=0),
        "Print Left": st.column_config.NumberColumn("Print Left", disabled=True),
        "Frame Done": st.column_config.NumberColumn("Frame Done", min_value=0),
        "Frame Left": st.column_config.NumberColumn("Frame Left", disabled=True),
    },
    use_container_width=True,
    hide_index=True
)

# Recalculate remaining values from user input dynamically
edited_df["Print Left"] = edited_df["Total Qty"] - edited_df["Print Done"]
edited_df["Frame Left"] = edited_df["Total Qty"] - edited_df["Frame Done"]

# Summary Section
st.markdown("---")
st.subheader("Production Progress Summary")

col1, col2 = st.columns(2)

with col1:
    total_print_left = int(edited_df["Print Left"].sum())
    st.metric(label="Blue (Print) Left", value=f"{total_print_left:,}")

with col2:
    total_frame_left = int(edited_df["Frame Left"].sum())
    st.metric(label="Green (Frame) Left", value=f"{total_frame_left:,}")
