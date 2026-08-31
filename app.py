import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Signage Production & Material Tracker", layout="wide")

st.title("Signage Production & Sheet Optimization Tracker")

# Setup Tabs
tab1, tab2 = st.tabs(["📋 Production Dashboard", "🧮 Chromadek Sheet Calculator"])

# --- TAB 1: PRODUCTION DASHBOARD ---
with tab1:
    st.header("Upload Signage Schedule")
    uploaded_file = st.file_uploader(
        "Upload Excel or CSV file", type=["xlsx", "xls", "csv"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)

            st.subheader("Data Preview & Mapping")
            st.dataframe(df_raw.head(), use_container_width=True)

            # Column Selectors
            col1, col2, col3 = st.columns(3)
            with col1:
                sign_col = st.selectbox(
                    "Select Sign Description/Name Column", df_raw.columns
                )
            with col2:
                qty_col = st.selectbox("Select Quantity Column", df_raw.columns)
            with col3:
                size_col = st.selectbox(
                    "Select Size/Dimensions Column (Optional)",
                    ["None"] + list(df_raw.columns),
                )

            # Process Base Data Frame
            production_df = pd.DataFrame()
            production_df["Sign Description"] = df_raw[sign_col]
            if size_col != "None":
                production_df["Size"] = df_raw[size_col]
            else:
                production_df["Size"] = "N/A"

            production_df["Total Required Qty"] = pd.to_numeric(
                df_raw[qty_col], errors="coerce"
            ).fillna(0)

            # Initialize Process Tracking Columns if not already present
            for process in ["Blue (Print)", "Green (Frame)", "Red (Laminate)", "Black (Plates)"]:
                production_df[f"{process} Finished"] = 0
                production_df[f"{process} Remaining"] = production_df["Total Required Qty"]

            st.markdown("---")
            st.subheader("Interactive Production Tracker")
            st.info(
                "Enter the finished quantities in the table below. The remaining counts will update automatically."
            )

            # Editable Dataframe Configuration
            column_config = {
                "Sign Description": st.column_config.TextColumn(disabled=True),
                "Size": st.column_config.TextColumn(disabled=True),
                "Total Required Qty": st.column_config.NumberColumn(disabled=True),
                "Blue (Print) Finished": st.column_config.NumberColumn(
                    label="Blue (Print) - Done", min_value=0, step=1
                ),
                "Blue (Print) Remaining": st.column_config.NumberColumn(
                    label="Blue (Print) - Left", disabled=True
                ),
                "Green (Frame) Finished": st.column_config.NumberColumn(
                    label="Green (Frame) - Done", min_value=0, step=1
                ),
                "Green (Frame) Remaining": st.column_config.NumberColumn(
                    label="Green (Frame) - Left", disabled=True
                ),
                "Red (Laminate) Finished": st.column_config.NumberColumn(
                    label="Red (Laminate) - Done", min_value=0, step=1
                ),
                "Red (Laminate) Remaining": st.column_config.NumberColumn(
                    label="Red (Laminate) - Left", disabled=True
                ),
                "Black (Plates) Finished": st.column_config.NumberColumn(
                    label="Black (Plates) - Done", min_value=0, step=1
                ),
                "Black (Plates) Remaining": st.column_config.NumberColumn(
                    label="Black (Plates) - Left", disabled=True
                ),
            }

            edited_df = st.data_editor(
                production_df,
                column_config=column_config,
                use_container_width=True,
                hide_index=True,
            )

            # Calculate Remaining Quantities Dynamically
            for process in ["Blue (Print)", "Green (Frame)", "Red (Laminate)", "Black (Plates)"]:
                edited_df[f"{process} Remaining"] = (
                    edited_df["Total Required Qty"] - edited_df[f"{process} Finished"]
                ).clip(lower=0)

            # Summary Metrics
            st.markdown("### Production Progress Summary")
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                total_blue_left = edited_df["Blue (Print) Remaining"].sum()
                st.metric(label="Blue (Print) Remaining", value=int(total_blue_left))
            with m2:
                total_green_left = edited_df["Green (Frame) Remaining"].sum()
                st.metric(label="Green (Frame) Remaining", value=int(total_green_left))
            with m3:
                total_red_left = edited_df["Red (Laminate) Remaining"].sum()
                st.metric(label="Red (Laminate) Remaining", value=int(total_red_left))
            with m4:
                total_black_left = edited_df["Black (Plates) Remaining"].sum()
                st.metric(label="Black (Plates) Remaining", value=int(total_black_left))

        except Exception as e:
            st.error(f"Error parsing file: {e}")
    else:
        st.info("Please upload a spreadsheet to begin tracking production.")

# --- TAB 2: CHROMADEK CALCULATOR ---
with tab2:
    st.header("Chromadek Sheet Requirement Calculator")
    st.caption("Standard Sheet Size: 2440 mm × 1220 mm | Includes 20% waste margin")

    # Sheet dimensions in mm
    SHEET_WIDTH = 2440
    SHEET_HEIGHT = 1220
    SHEET_AREA = SHEET_WIDTH * SHEET_HEIGHT  # sq mm

    col_input1, col_input2 = st.columns(2)
    with col_input1:
        margin_percent = st.number_input(
            "Waste / Over-cut Margin (%)", value=20.0, step=1.0
        )
    with col_input2:
        custom_sheet = st.selectbox(
            "Sheet Size", ["Standard 2440 x 1220 mm", "Custom Dimensions"]
        )

    if custom_sheet == "Custom Dimensions":
        c_w = st.number_input("Sheet Width (mm)", value=2440)
        c_h = st.number_input("Sheet Height (mm)", value=1220)
        SHEET_AREA = c_w * c_h

    st.subheader("Sign Inventory Input")
    st.write("Enter sign panel dimensions (mm) and quantities to calculate total full sheets:")

    # Default structure for sheet calculation
    default_calc_data = pd.DataFrame(
        [
            {"Width (mm)": 600, "Height (mm)": 450, "Quantity": 10},
            {"Width (mm)": 1200, "Height (mm)": 900, "Quantity": 4},
        ]
    )

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

    # Calculate Total Area Required
    calc_df["Area per Sign (sq mm)"] = calc_df["Width (mm)"] * calc_df["Height (mm)"]
    calc_df["Total Area (sq mm)"] = calc_df["Area per Sign (sq mm)"] * calc_df["Quantity"]

    net_area_sq_mm = calc_df["Total Area (sq mm)"].sum()
    net_area_sq_m = net_area_sq_mm / 1,000,000

    # Apply 20% waste margin
    gross_area_sq_mm = net_area_sq_mm * (1 + (margin_percent / 100))
    gross_area_sq_m = gross_area_sq_mm / 1,000,000

    sheets_raw = gross_area_sq_mm / SHEET_AREA
    sheets_required = math.ceil(sheets_raw)

    st.markdown("---")
    st.subheader("Material Requirements")

    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric(label="Net Area (Signs Only)", value=f"{net_area_sq_m:.2f} m²")
    with res_col2:
        st.metric(
            label=f"Gross Area (+{margin_percent}% Margin)",
            value=f"{gross_area_sq_m:.2f} m²",
        )
    with res_col3:
        st.metric(
            label="Total Chromadek Sheets Required",
            value=f"{sheets_required} Sheets",
            delta=f"Raw fit: {sheets_raw:.2f}",
        )
