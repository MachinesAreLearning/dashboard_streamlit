# app.py

import streamlit as st
import pandas as pd
from dashboard_styles import get_dashboard_styles
from data_processor import (
    load_and_filter_data, 
    calculate_main_metrics, 
    calculate_category_metrics,
    get_subcategory_metrics
)

# Set page configuration
st.set_page_config(layout="wide")

# Apply styles
st.markdown(get_dashboard_styles(), unsafe_allow_html=True)

# Header
st.markdown('<div class="blue-header"><h3>Consumer Banking Branch Manager Scorecard</h3></div>', unsafe_allow_html=True)

# Load initial data
df = load_and_filter_data()

# Get unique values for filters
divisions = ['All'] + sorted(df['Division'].unique().tolist())
regions = ['All'] + sorted(df['Region'].unique().tolist())
markets = ['All Markets'] + sorted(df['Market'].unique().tolist())

# Region selector with spacing
col1, col2, col3, spacing, col4, spacing2, col5 = st.columns([1, 1, 1, 0.3, 1, 2.5, 1])
with col1:
    division = st.selectbox("Division", divisions)
with col2:
    region = st.selectbox("Region", regions)
with col3:
    market = st.selectbox("Market", markets)
with col4:
    st.checkbox("save as default", key="disabled")
with col5:
    st.button("Export to PDF")

# Filter data based on selections
filtered_df = load_and_filter_data(division, region, market)

# Calculate metrics
main_metrics = calculate_main_metrics(filtered_df)

# Helper functions for creating metric boxes
def create_metric_box(label, value):
    return f"""
    <div class="metric-container">
        <div class="ytd-label-top">YTD</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

def create_metric_box_wrapped(label, value):
    return f"""
    <div class="metric-container">
        <div class="ytd-label-top">YTD</div>
        <div class="metric-label-2">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

# Display main metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(create_metric_box(
        "Overall Weighted Score", 
        f"{main_metrics['overall_score']:.2f}%"
    ), unsafe_allow_html=True)
with col2:
    st.markdown(create_metric_box(
        "Overall Rank", 
        str(main_metrics['overall_rank'])
    ), unsafe_allow_html=True)
with col3:
    st.markdown(create_metric_box_wrapped(
        "% of Branches in PL 1/2 vs. PL 5/6",
        main_metrics['pl_distribution']
    ), unsafe_allow_html=True)

# Calculate and display category metrics
category_metrics = calculate_category_metrics(filtered_df)

def create_comparison_metric(value):
    is_positive = not str(value).startswith('-')
    color_class = "positive-value" if is_positive else "negative-value"
    arrow_class = "arrow-up" if is_positive else "arrow-down"
    return f'<span class="{color_class} {arrow_class}">{value}</span>'

# Display category metrics boxes
col1, col2, col3, col4, col5 = st.columns(5)
columns = [col1, col2, col3, col4, col5]

for i, (category, data) in enumerate(category_metrics.items()):
    with columns[i]:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-header-row">
                <div class="metric-title">{category}</div>
                <div class="metric-percentage">{data['value']:.2f}%</div>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {min(data['value'] * 2, 100)}%; background-color: {data['color']};"></div>
            </div>
            <div class="comparison-section">
                <div class="comparison-labels">
                    <span>vs Last month</span>
                    <span>Peer group</span>
                    <span>National</span>
                </div>
                <div class="comparison-values">
                    {create_comparison_metric(data['vs_last'])}
                    {create_comparison_metric(data['peer'])}
                    {create_comparison_metric(data['national'])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Function to display metrics tables
def display_metrics_table(title, metrics_data):
    table_html = f"""
    <div class="metric-box">
        <div class="table-header"><h6>{title}</h6></div>
        <table class="metric-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>YTD Sep 24</th>
                    <th>Metric Score</th>
                    <th>Weight</th>
                    <th>Weighted Score</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for metric in metrics_data:
        table_html += f"""
                <tr>
                    <td style="text-align: left">{metric['Metric']}</td>
                    <td style="text-align: right">{metric['YTD Sep 24']}</td>
                    <td style="text-align: right">{metric['Metric Score']}</td>
                    <td style="text-align: right">{metric['Weight']}</td>
                    <td style="text-align: right">{metric['Weighted Score']}</td>
                </tr>
        """
    
    table_html += """
            </tbody>
        </table>
    </div>
    """
    
    return st.markdown(table_html, unsafe_allow_html=True)

# Display tables in pairs
categories = list(category_metrics.keys())

# First row of tables
col1, col2 = st.columns(2)
with col1:
    metrics = get_subcategory_metrics(filtered_df, "Growth & One Chase")
    display_metrics_table("Growth & One Chase", metrics)

with col2:
    metrics = get_subcategory_metrics(filtered_df, "Customer Experience")
    display_metrics_table("Customer Experience", metrics)

# Second row of tables
col3, col4 = st.columns(2)
with col3:
    metrics = get_subcategory_metrics(filtered_df, "Financial Health & Innovation")
    display_metrics_table("Financial Health & Innovation", metrics)

with col4:
    metrics = get_subcategory_metrics(filtered_df, "Culture & Employee")
    display_metrics_table("Culture & Employee", metrics)

# Last table
col5, _ = st.columns(2)
with col5:
    metrics = get_subcategory_metrics(filtered_df, "Controls")
    display_metrics_table("Controls", metrics)