import pandas as pd
import plotly.express as px
import streamlit as st

def plot_level_distribution(df):
    counts = df["level"].value_counts()
    fig = px.pie(names=counts.index, values=counts.values, title="Log Level Distribution")
    st.plotly_chart(fig)

def plot_timeline(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    counts = df.groupby(pd.Grouper(key="timestamp", freq="1min")).size().reset_index(name="count")
    fig = px.line(counts, x="timestamp", y="count", title="Log Events Over Time")
    st.plotly_chart(fig)

def show_table(df):
    st.dataframe(df)

def compare_files(dfs, filenames):
    st.header("📊 Comparison")
    for df, name in zip(dfs, filenames):
        st.subheader(name)
        if "level" in df.columns:
            plot_level_distribution(df)
        if "timestamp" in df.columns:
            plot_timeline(df)
            show_alerts(df, 50)
        show_table(df)

def show_alerts(df, threshold):
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    if len(df) > 0:
        counts = df.groupby(pd.Grouper(key="timestamp", freq="5min")).size()
        if any(counts > threshold):
            st.error(f"🚨 ALERT: More than {threshold} events detected in a 5-minute window!")
