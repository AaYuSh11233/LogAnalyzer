import streamlit as st
import pandas as pd
from db import query_logs
from log_parser import load_log_to_db
from utils import show_header, export_report
from visualizer import plot_level_distribution, plot_timeline, show_table, show_alerts

def main():
    show_header()
    
    mode = st.sidebar.selectbox(
        "Choose mode",
        ["Upload & Analyze", "Monitor Directory"]
    )

    if mode == "Upload & Analyze":
        uploaded_files = st.file_uploader(
            "Choose one log file", type=["log", "txt", "csv", "json"], accept_multiple_files=False
        )

        if uploaded_files:
            with open(f"temp_{uploaded_files.name}", "wb") as f:
                f.write(uploaded_files.read())
            load_log_to_db(f"temp_{uploaded_files.name}")

            st.success("Loaded log into database.")

            rows = query_logs()
            if rows:
                df = pd.DataFrame(rows, columns=["timestamp", "level", "message"])
                st.write(f"Showing first {len(df)} rows")
                if "level" in df.columns:
                    plot_level_distribution(df)
                if "timestamp" in df.columns:
                    plot_timeline(df)
                    show_alerts(df, 50)
                show_table(df)
                export_report(df, uploaded_files.name)
    
    elif mode == "Monitor Directory":
        st.info("Directory monitoring feature coming soon!")

if __name__ == "__main__":
    main()
