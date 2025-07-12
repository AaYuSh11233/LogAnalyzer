import pandas as pd
import streamlit as st

def show_header():
    st.title("📊 Log Analyzer & Visualizer")
    st.markdown("""
    Upload or monitor `.log`, `.txt`, `.csv`, or `.json` files and visualize the events.
    """)

def export_report(df, filename_base):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Report (Excel)"):
            out = f"{filename_base}_report.xlsx"
            df.to_excel(out, index=False)
            with open(out, "rb") as f:
                st.download_button("Download Excel Report", f, file_name=out)

    with col2:
        if st.button("Export Report (CSV)"):
            out = f"{filename_base}_report.csv"
            df.to_csv(out, index=False)
            with open(out, "rb") as f:
                st.download_button("Download CSV Report", f, file_name=out)
