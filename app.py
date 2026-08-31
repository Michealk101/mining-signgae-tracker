import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Dishaba Mine Signage Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("Dishaba Mine - Signage Production Tracker")
st.write("Enter the finished quantities in the table below. The remaining counts will update automatically.")

# Embedded Master Data (All 271 items across all shafts)
DEFAULT_DATA = [
    {"Sheet": "2 Shaft", "Area": "2 Shaft", "DESCRIPTION": "Road signs", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "2 Shaft", "DESCRIPTION": "2# Fridge Plant", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "2 Shaft", "DESCRIPTION": "2# RO Plant", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "2 Shaft", "DESCRIPTION": "2# Compressors", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "2 Shaft", "DESCRIPTION": "2# Lamproom", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Industrial Changehouses", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "2# Settling Pond", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Oxygen/Acetylene", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Hazourdous waste", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Pipes signs 1\", 2\", 4\", 8\", 10\"", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Ventilation pipe", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Explosive delivery bay", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Rail", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Stope timber", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "2# notice board", "Total Qty": 8},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Plan board", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Dishaba mine - Notice board", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "Safety notice board", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "Bank area", "DESCRIPTION": "This area is under surveilance", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "10 Level haulage sign", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "High pressure door", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Brake test area", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Explosives accessory bay", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Refuge bay -10/40,43,50,55,46,44,48", "Total Qty": 10},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "End of section", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "10 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "11 Level haulage sign", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "High pressure door", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Brake test area", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Explosives accessory bay", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "End of section", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "11 Level", "DESCRIPTION": "12 Level haulage sign", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "High pressure door", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Brake test area", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 2},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 9},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "End of section", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "12 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "13 Level haulage sign", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "High pressure door", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Brake test area", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Local transformer 11kV", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Lighting transformer 525V", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Aux transformer 11kV", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Converter transformer 11kV", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "13 Level main substation", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Bundwalls", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "13level  footwall panel", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "End of section", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "14 Level haulage sign", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "High pressure door", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "13 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "Brake test area", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "Explosives accessory bay", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "End of section", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "14 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "15 Level haulage sign", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "High pressure door", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Brake test area", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "End of section", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "15 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "16 Level haulage sign", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "High pressure door", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 2},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Brake test area", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "End of section", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "16 Level", "DESCRIPTION": "17 Level haulage sign", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "High pressure door", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Brake test area", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "End of section", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "17 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "18 Level haulage sign", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "High pressure door", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Brake test area", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 7},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "End of section", "Total Qty": 2},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 2},
    {"Sheet": "2 Shaft", "Area": "18 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 2},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "19 Level haulage sign", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "High pressure door", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Brake test area", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 6},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "End of section", "Total Qty": 2},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 2},
    {"Sheet": "2 Shaft", "Area": "19 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 2},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "20 Level haulage sign", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "No self prepelled vehicles", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Emergency assembly point", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "High pressure door", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Rail management plan", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Traffic management plan", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Battery bay notice board", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Maximum permissible loads", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "No riding in hoppper", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Brake test area", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Waste and Reef Main Tip", "Total Qty": 3},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Our life saving golden rules", "Total Qty": 4},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Refuge bay", "Total Qty": 5},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "End of section", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Section 23 MHSA", "Total Qty": 1},
    {"Sheet": "2 Shaft", "Area": "20 Level", "DESCRIPTION": "Section 22 MHSA", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba", "DESCRIPTION": "Oil storex5 / Paint Storex5 / Chemical Storex5", "Total Qty": 15},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "61 FAN mini sub 1 1000V FEED FROM O/H LINE2", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "61 FAN TRANSFORMER BAY N0.1 11KV/0.55KV FEED FROM 61 FAN MINI-SUB 11000V", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "61 FAN TRANSFORMER BAY N0.2 11KV/0.55KV FEED FROM 61 FAN MINI-SUB 11000V", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "61 FANS", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 EAST SURFACE SUBSTATION 11000 VOLTS", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 EAST CONVERTER TX", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 EAST MINI SUBSTATION", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 EAST AUXILARY TX", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 EAST LIGHTING TX", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 EAST MINI SUBSTATION", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 EAST CONVERTER TX", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 SHAFT 3 LEVEL SUB-STATION", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 SHAFT 4 LEVEL SUB-STATION", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 SHAFT 4 LEVEL SUB-STATION 11KV FEED FROM 3 LEVEL", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "62 SHAFT 5 LEVEL SUB-STATION", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 SHAFT 5 LEVEL SUB-STATION 11 11KV FEED FROM 4 LEVEL", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 SHAFT 5 LEVEL SUBSTATION", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 EAST 5 LEVEL SUBSTATION 1100V, FEED FROM 50 EAST 4 LEVEL SUB-STATION 11000V PANEL2", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 SHAFT 6 LEVEL SUBSTATION 11KV FEED FROM 7 LEVEL", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 EAST 6 LEVEL SUBSTATION 11000V, FEED FROM 50 EAST 5 LEVEL SUB-STATION 11000V PANEL 3", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 SHAFT  7 LEVEL SUBSTATION 11KV FEED FROM SURFACE", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 EAST 7 LEVEL SUBSTATION 11000V PANEL N0.5, RING FEED FROM 50 EAST F/WALL SUBSTATION 11", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 SHAFT 4 LEVEL SUBSTATION 11KV FEED FROM 3 LEVEL", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 EAST 4 LEVEL SUBSTATION 11000V FEED FROM 50 EAST 3 LEVEL SUB-STATION 11000V PANEL 4", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 SHAFT 3 LEVEL SUBSTATION 11KV FEED FROM SURFACE", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "RESPONSIBLE PERSON FOR THIS AREA", "Total Qty": 6},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 EAST 3 LEVEL SUBSTATION 11000V PANEL NO 6", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "BUDWALL CAPACITY, OIL CAPACITY", "Total Qty": 10},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "50 WINDER SIGN", "Total Qty": 2},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "MSDS Combo", "Total Qty": 6},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "Bund Wall Capacity", "Total Qty": 30},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "Cylinders MSDS", "Total Qty": 10},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper Undergroun d Signs", "DESCRIPTION": "Oxygen and Acetylene", "Total Qty": 10},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "1. Visitors parking area", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "2. Dishaba Mock-up area", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "3. 49E turf dam", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "4. 50E Rosond plant", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "5. 59E Rosond plant", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "6. 50E Erickson dams", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "7. 50 shaft chairlift", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "8. 50FW winder", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "9. 62 FW winder", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "10. 62# bank", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "11. 50# bank", "Total Qty": 5},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "12. 62 workshop", "Total Qty": 6},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "Directional signage: At 50 cross over...", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "Directional signage: In front of 50 chairlift...", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "49E turf dam (point to the right)", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "Directional signage: 62 turn...", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Upper  Road Signage", "DESCRIPTION": "Directional signage: 59 turn...", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Lower", "DESCRIPTION": "ENGINEERING BATTERY BAY NOTICE BOARD LEVEL 11,12,13&14", "Total Qty": 4},
    {"Sheet": "Dishaba", "Area": "Dishaba Lower", "DESCRIPTION": "OPERATIONAL CONTROL ROOM SIGN", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Lower", "DESCRIPTION": "CONTROL ROOM SIGN", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Lower", "DESCRIPTION": "EMERGENCY CONTROL ROOM SIGN", "Total Qty": 1},
    {"Sheet": "Dishaba", "Area": "Dishaba Lower", "DESCRIPTION": "BATTERY BAY NOTICE BOARD LEVEL 11,12,13&14", "Total Qty": 4},
    {"Sheet": "Dishaba", "Area": "Dishaba Lower", "DESCRIPTION": "WORKSHOP NOTICE BOARD LEVEL 11,12,13,&14", "Total Qty": 4},
    {"Sheet": "Dishaba", "Area": "Dishaba Lower", "DESCRIPTION": "Dishaba Upper underground Loco & Loader Service signs", "Total Qty": 10},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Chairlift safety signs (each level)", "Total Qty": 7},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "4/40, 4/43,4/44,4/45, 4/48 Refuge bay - Reflective", "Total Qty": 5},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "6 Level main substation - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "7 Level haulage sign - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Rail management plan - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Traffic management plan - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Our life saving golden rules - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "8 Level haulage sign - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Rail management plan - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Traffic management plan - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Our life saving golden rules - Reflective", "Total Qty": 9},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "9 Level haulage sign - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Rail management plan - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Traffic management plan - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Battery bay notice board - Reflective", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Our life saving golden rules - Reflective", "Total Qty": 9},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Chairlift safety signs (each level)", "Total Qty": 10},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Battery bay notice board", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Brake test area", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Traffic management plan", "Total Qty": 1},
    {"Sheet": "Dishaba 44 & 50 Shaft", "Area": "Dishaba 44 & 50 Shaft", "DESCRIPTION": "Waste & main tip", "Total Qty": 2}
]

# Persistent Session State initialization
if "df_master" not in st.session_state:
    df_init = pd.DataFrame(DEFAULT_DATA)
    df_init["Print Done"] = 0
    df_init["Lam Done"] = 0
    df_init["Plates Done"] = 0
    df_init["Frame Done"] = 0
    st.session_state.df_master = df_init

# Recalculate dynamic columns on the master session dataframe
st.session_state.df_master["Print Left"] = st.session_state.df_master["Total Qty"] - st.session_state.df_master["Print Done"]
st.session_state.df_master["Lam Left"] = st.session_state.df_master["Total Qty"] - st.session_state.df_master["Lam Done"]
st.session_state.df_master["Plates Left"] = st.session_state.df_master["Total Qty"] - st.session_state.df_master["Plates Done"]
st.session_state.df_master["Frame Left"] = st.session_state.df_master["Total Qty"] - st.session_state.df_master["Frame Done"]

# Sidebar view selector
shaft_options = ["All Shafts Combined", "2 Shaft", "Dishaba", "Dishaba 44 & 50 Shaft"]
selected_view = st.sidebar.selectbox("Select Shaft / Section View", shaft_options)

# Filter data based on sidebar selection
if selected_view == "All Shafts Combined":
    filter_mask = pd.Series(True, index=st.session_state.df_master.index)
else:
    filter_mask = st.session_state.df_master["Sheet"] == selected_view

display_df = st.session_state.df_master[filter_mask].copy()

# Columns arrangement
cols = [
    "Area", "DESCRIPTION", "Total Qty",
    "Print Done", "Print Left",
    "Lam Done", "Lam Left",
    "Plates Done", "Plates Left",
    "Frame Done", "Frame Left"
]
display_df = display_df[[c for c in cols if c in display_df.columns]]

# Interactive Data Editor
edited_df = st.data_editor(
    display_df,
    column_config={
        "Area": st.column_config.TextColumn("Area", disabled=True),
        "DESCRIPTION": st.column_config.TextColumn("Description", disabled=True),
        "Total Qty": st.column_config.NumberColumn("Total Qty", disabled=True),
        "Print Done": st.column_config.NumberColumn("Print Done", min_value=0),
        "Print Left": st.column_config.NumberColumn("Print Left", disabled=True),
        "Lam Done": st.column_config.NumberColumn("Lamination Done", min_value=0),
        "Lam Left": st.column_config.NumberColumn("Lamination Left", disabled=True),
        "Plates Done": st.column_config.NumberColumn("Plates Done", min_value=0),
        "Plates Left": st.column_config.NumberColumn("Plates Left", disabled=True),
        "Frame Done": st.column_config.NumberColumn("Frame Done", min_value=0),
        "Frame Left": st.column_config.NumberColumn("Frame Left", disabled=True),
    },
    use_container_width=True,
    hide_index=True,
    key=f"editor_{selected_view}"
)

# Update persistent session state with user edits
st.session_state.df_master.loc[filter_mask, ["Print Done", "Lam Done", "Plates Done", "Frame Done"]] = edited_df[["Print Done", "Lam Done", "Plates Done", "Frame Done"]].values

# Recalculate remaining counts dynamically after state update
st.session_state.df_master["Print Left"] = st.session_state.df_master["Total Qty"] - st.session_state.df_master["Print Done"]
st.session_state.df_master["Lam Left"] = st.session_state.df_master["Total Qty"] - st.session_state.df_master["Lam Done"]
st.session_state.df_master["Plates Left"] = st.session_state.df_master["Total Qty"] - st.session_state.df_master["Plates Done"]
st.session_state.df_master["Frame Left"] = st.session_state.df_master["Total Qty"] - st.session_state.df_master["Frame Done"]

# Summary Metrics
st.markdown("---")
st.subheader("Production Progress Summary")

current_summary_df = st.session_state.df_master[filter_mask]

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Signage Items", f"{int(current_summary_df['Total Qty'].sum()):,}")
with col2:
    st.metric("Print Left", f"{int(current_summary_df['Print Left'].sum()):,}")
with col3:
    st.metric("Lamination Left", f"{int(current_summary_df['Lam Left'].sum()):,}")
with col4:
    st.metric("Plates Left", f"{int(current_summary_df['Plates Left'].sum()):,}")
with col5:
    st.metric("Frame Left", f"{int(current_summary_df['Frame Left'].sum()):,}")
