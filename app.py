import os
import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Signage Production & Material Tracker", layout="wide")

st.title("Signage Production & Sheet Optimization Tracker")

# Path for persistent local storage file
SAVE_FILE_PATH = "saved_progress.csv"

# Function to load stored progress from file
def load_saved_data():
    if os.path.exists(SAVE_FILE_PATH):
        try:
            return pd.read_csv(SAVE_FILE_PATH)
        except Exception:
            return None
    return None

# Function to write active progress to file
def save_data_to_disk(df):
    try:
        df.to_csv(SAVE_FILE_PATH, index=False)
        st.toast("Progress saved to storage!", icon="💾")
    except Exception as e:
        st.error(f"Failed to save progress: {e}")

# Setup Tabs
tab1, tab2 = st.tabs(["📋 Production Dashboard", "🧮 Chromadek Sheet Calculator"])

# --- TAB 1: PRODUCTION DASHBOARD ---
with tab1:
    st.header("Upload or Load Signage Schedule")
    
    # Load any previously saved session from disk on app launch
    saved_df = load_saved_data()
    
    col_file, col_status = st.columns([2, 1])
    with col_file:
        uploaded_file = st.file_uploader(
            "Upload Excel or CSV file (Uploading a new file resets current progress)",
            type=["xlsx", "xls", "csv"]
        )

    # 1. PROCESS NEW FILE UPLOAD
    if uploaded_file is not None:
        file_key = f"file_{uploaded_file.name}_{uploaded_file.size}"
        if "last_file_key" not in st.session_state or st.session_state["last_file_key"] != file_key:
            st.session_state["last_file_key"] = file_key
            
            if uploaded_file.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)

            cols = list(df_raw.columns)

            def find_best_match(keywords, default_idx=0):
                for col in cols:
                    if any(k.lower() in str(col).lower() for k in keywords):
                        return col
                return cols[default_idx] if cols else None

            default_sign = find_best_match(["sign", "description", "item", "name"], 0)
            default_qty = find_best_match(["qty", "quantity", "count", "amount", "total"], min(1, len(cols)-1))
            default_size = find_best_match(["size", "dimension", "dim", "mm"], 0)

            base_df = pd.DataFrame()
            base_df["Sign Description"] = df_raw[default_sign].astype(str)
            base_df["Size"] = df_raw[default_size].astype(str) if default_size else "N/A"
            base_df["Total Required Qty"] = pd.to_numeric(df_raw[default_qty], errors="coerce").fillna(0).astype(int)

            processes = ["Blue (Print)", "Green (Frame)", "Red (Laminate)", "Black (Plates)"]
            for process in processes:
                base_df[f"{process} Finished"] = 0
                base_df[f"{process} Remaining"] = base_df["Total Required Qty"]

            st.session_state["production_df"] = base_df
            save_data_to_disk(base_df)

    # 2. RESTORE FROM DISK IF NO NEW UPLOAD
    elif "production_df" not in st.session_state:
        if saved_df is not None:
            st.session_state["production_df"] = saved_df
            st.success("Restored active progress from last session!")

    # 3. RENDER TRACKER IF DATA IS AVAILABLE
    if "production_df" in st.session_state:
        st.markdown("---")
        st.subheader("Interactive Production Tracker")
        
        btn_col1, btn_col2 = st.columns([1, 4])
        with btn_col1:
            if st.button("💾 Save Progress Now"):
                save_data_to_disk(st.session_state["production_df"])

        processes = ["Blue (Print)", "Green (Frame)", "Red (Laminate)", "Black (Plates)"]

        column_config = {
            "Sign Description": st.column_config.TextColumn(disabled=True),
            "Size": st.column_config.TextColumn(disabled=True),
            "Total Required Qty": st.column_config.NumberColumn("Total Qty", disabled=True),
            "Blue (Print) Finished": st.column_config.NumberColumn("Print Done", min_value=0, step=1),
            "Blue (Print) Remaining": st.column_config.NumberColumn("Print Left", disabled=True),
            "Green (Frame) Finished": st.column_config.NumberColumn("Frame Done", min_value=0, step=1),
            "Green (Frame) Remaining": st.column_config.NumberColumn("Frame Left", disabled=True),
            "Red (Laminate) Finished": st.column_config.NumberColumn("Lam. Done", min_value=0, step=1),
            "Red (Laminate) Remaining": st.column_config.NumberColumn("Lam. Left", disabled=True),
            "Black (Plates) Finished": st.column_config.NumberColumn("Plates Done", min_value=0, step=1),
            "Black (Plates) Remaining": st.column_config.NumberColumn("Plates Left", disabled=True),
        }

        edited_df = st.data_editor(
            st.session_state["production_df"],
            column_config=column_config,
            use_container_width=True,
            hide_index=True,
            key="editor"
        )

        # Recalculate remaining quantities dynamically
        for process in processes:
            edited_df[f"{process} Remaining"] = (
                edited_df["Total Required Qty"] - edited_df[f"{process} Finished"]
            ).clip(lower=0)

        # Auto-update state & save directly to disk
        st.session_state["production_df"] = edited_df
        save_data_to_disk(edited_df)

        st.markdown("### Production Progress Summary")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Blue (Print) Left", int(edited_df["Blue (Print) Remaining"].sum()))
        with m2:
            st.metric("Green (Frame) Left", int(edited_df["Green (Frame) Remaining"].sum()))
        with m3:
            st.metric("Red (Laminate) Left", int(edited_df["Red (Laminate) Remaining"].sum()))
        with m4:
            st.metric("Black (Plates) Left", int(edited_df["Black (Plates) Remaining"].sum()))

    else:
        st.info("Upload a spreadsheet file above to start tracking production.")

# --- TAB 2: CHROMADEK CALCULATOR ---
with tab2:
    st.header("Chromadek Sheet Calculator")
    st.caption("Standard Sheet Size: 2440 mm × 1220 mm | Includes 20% safety margin")

    SHEET_WIDTH = 2440
    SHEET_HEIGHT = 1220
    SHEET_AREA = SHEET_WIDTH * SHEET_HEIGHT

    c1, c2 = st.columns(2)
    with c1:
        margin_percent = st.number_input("Waste / Cut Margin (%)", value=20.0, step=1.0)
    with c2:
        custom_sheet = st.selectbox("Sheet Size Preset", ["Standard 2440 x 1220 mm", "Custom Dimensions"])

    if custom_sheet == "Custom Dimensions":
        c_w = st.number_input("Sheet Width (mm)", value=2440)
        c_h = st.number_input("Sheet Height (mm)", value=1220)
        SHEET_AREA = c_w * c_h

    st.subheader("Sign Inventory Input")

    default_calc_data = pd.DataFrame([
        {"Width (mm)": 600, "Height (mm)": 450, "Quantity": 10},
        {"Width (mm)": 1200, "Height (mm)": 900, "Quantity": 4},
    ])

    calc_df = st.data_editor(
        default_calc_data,
        num_rows="dynamic",
        column_config={
            "Width (mm)": st.column_config.NumberColumn(min_value=1, step=10),
            "Height (mm)": st.column_config.NumberColumn(min_value=1, step=10),
            "Quantity": st.column_config.NumberColumn(min_value=1, step=1),
        },
        use_container_width=True,
    )

    calc_df["Area per Sign (sq mm)"] = calc_df["Width (mm)"] * calc_df["Height (mm)"]
    calc_df["Total Area (sq mm)"] = calc_df["Area per Sign (sq mm)"] * calc_df["Quantity"]

    net_area_sq_mm = calc_df["Total Area (sq mm)"].sum()
    net_area_sq_m = net_area_sq_mm / 1000000

    gross_area_sq_mm = net_area_sq_mm * (1 + (margin_percent / 100))
    gross_area_sq_m = gross_area_sq_mm / 1000000

    sheets_raw = gross_area_sq_mm / SHEET_AREA
    sheets_required = math.ceil(sheets_raw)

    st.markdown("---")
    st.subheader("Results")

    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric("Net Area", f"{net_area_sq_m:.2f} m²")
    with res_col2:
        st.metric(f"Gross Area (+{margin_percent}%)", f"{gross_area_sq_m:.2f} m²")
    with res_col3:
        st.metric("Sheets Needed", f"{sheets_required} Sheets")
