import streamlit as st
import pandas as pd
import numpy as np
from styles import get_dashboard_styles, get_table_styles
from utils import (create_metric_box, create_metric_box_0, create_comparison_metric, 
                  calculate_comparison, style_dataframe)
from config import METRICS_CONFIG, TABLE_CONFIGS

# Set page configuration
st.set_page_config(layout="wide")

# Apply styles
st.markdown(get_dashboard_styles(), unsafe_allow_html=True)
st.markdown(get_table_styles(), unsafe_allow_html=True)

# Header
st.markdown('<div class="blue-header"><h3>Consumer Banking Branch Manager Scorecard</h3></div>', unsafe_allow_html=True)

# Region selector with spacing
col1, col2, col3, col4, spacing, col5, spacing, col6 = st.columns([1, 1, 1, 1, 0.3, 1, 2.5, 1])

# Checkbox for actual data (moved before data loading)
with col5:
    show_actual = st.checkbox("Show Actual", key="show_actual")

# Load data
@st.cache_data
def load_data(is_actual=False):
    try:
        if is_actual:
            return pd.read_csv('branch_data_actual.csv')
        return pd.read_csv('branch_data.csv')
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Load appropriate dataset
df = load_data(show_actual)

# Division selector
division_options = ['All Divisions'] + list(df['Division'].unique()) if not df.empty else ['All Divisions']
with col1:
    division = st.selectbox("Division", options=division_options, index=0)

# Filter regions based on selected division
with col2:
    if division == 'All Divisions':
        region_options = ['All Regions'] + list(df['Region'].unique())
    else:
        region_options = ['All Regions'] + list(df[df['Division'] == division]['Region'].unique())
    region = st.selectbox("Region", options=region_options, index=0)

# Filter markets based on selected region
with col3:
    if region == 'All Regions':
        if division == 'All Divisions':
            market_options = ['All Markets'] + list(df['Market'].unique())
        else:
            market_options = ['All Markets'] + list(df[df['Division'] == division]['Market'].unique())
    else:
        market_options = ['All Markets'] + list(df[df['Region'] == region]['Market'].unique())
    market = st.selectbox("Market", options=market_options, index=0)

# Filter branches based on selections
with col4:
    if market == 'All Markets':
        if region == 'All Regions':
            if division == 'All Divisions':
                branch_options = ['All Branches'] + list(df['Branch'].unique())
            else:
                branch_options = ['All Branches'] + list(df[df['Division'] == division]['Branch'].unique())
        else:
            branch_options = ['All Branches'] + list(df[df['Region'] == region]['Branch'].unique())
    else:
        branch_options = ['All Branches'] + list(df[df['Market'] == market]['Branch'].unique())
    branch = st.selectbox("Branch", options=branch_options, index=0)

with col6:
    st.button("Export to PDF")
# Get filtered data
def get_filtered_data():
    """Get filtered dataframe based on selected filters"""
    filtered_df = df.copy()
    
    # Apply filters only if specific selections are made
    if division != 'All Divisions':
        filtered_df = filtered_df[filtered_df['Division'] == division]
    if region != 'All Regions':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if market != 'All Markets':
        filtered_df = filtered_df[filtered_df['Market'] == market]
    if branch != 'All Branches':
        filtered_df = filtered_df[filtered_df['Branch'] == branch]
    
    # Show message if no specific selections are made
    if all(x.startswith('All') for x in [division, region, market, branch]):
        st.info("👆 Select specific Division, Region, Market, or Branch to filter the data.")
    
    return filtered_df

# Get filtered data
filtered_df = get_filtered_data()

# Optional debug info
if st.checkbox("Show Debug Info", key="debug"):
    st.write("Filtered Data Shape:", filtered_df.shape)
    st.write("Applied Filters:", {
        "Division": division,
        "Region": region,
        "Market": market,
        "Branch": branch
    })

# Place this code after your filter section and before the performance metrics display

# After filtered_df = get_filtered_data()

def calculate_pl_distribution(filtered_df):
    """
    Calculate PL distribution for the filtered dataset
    If all filters are "All", uses complete dataset
    Otherwise uses filtered dataset
    """
    try:
        # Use filtered data for calculation
        total_branches = len(filtered_df)
        if total_branches == 0:
            return "N/A"
        
        # Calculate PL distributions
        pl_12_count = len(filtered_df[filtered_df['Performance_Level'].isin([1, 2])])
        pl_56_count = len(filtered_df[filtered_df['Performance_Level'].isin([5, 6])])
        
        pl_12_pct = (pl_12_count / total_branches) * 100
        pl_56_pct = (pl_56_count / total_branches) * 100
        
        return f"{pl_12_pct:.1f}% / {pl_56_pct:.1f}%"
    except Exception as e:
        st.error(f"Error calculating PL distribution: {str(e)}")
        return "N/A"

# Display main metrics
col1, col2, col3 = st.columns(3)
with col1:
    overall_score = filtered_df['gofirsttime-wt'].mean()
    st.markdown(create_metric_box("Overall Weighted Score", f"{overall_score:.2f}%"), unsafe_allow_html=True)

with col2:
    rank = filtered_df['overall_rank'].iloc[0] if not filtered_df.empty else "N/A"
    st.markdown(create_metric_box("Overall Rank", rank), unsafe_allow_html=True)

with col3:
    pl_dist = calculate_pl_distribution(df)
    st.markdown(create_metric_box_0("% of Branches in PL 1/2 vs. PL 5/6", pl_dist), unsafe_allow_html=True)

# Display performance metrics
col1, col2, col3, col4, col5 = st.columns(5)
columns = [col1, col2, col3, col4, col5]

for i, (metric, config) in enumerate(METRICS_CONFIG.items()):
    with columns[i]:
        value = filtered_df[config['score_column']].mean() if config['score_column'] in filtered_df.columns else 0
        fill_percentage = min((value / config['max_value']) * 100, 100)
        
        comparisons = {
            key: calculate_comparison(filtered_df, col) 
            for key, col in config['comparison_columns'].items()
        }
        
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title" style="font-weight: 600;">{metric}</div>
            <div class="metric-percentage">{value:.2f}%</div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {fill_percentage}%; background-color: {config['color']};"></div>
            </div>
            <div class="comparison-section">
                <div class="comparison-labels">
                    <span>vs Last month</span>
                    <span>Peer group</span>
                    <span>National</span>
                </div>
                <div class="comparison-values">
                    {create_comparison_metric(comparisons['vs_last'])}
                    {create_comparison_metric(comparisons['peer'])}
                    {create_comparison_metric(comparisons['national'])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Display metric tables
def create_metrics_table(filtered_df, table_type):
    config = TABLE_CONFIGS[table_type]
    
    data = {
        'Metric': [m['name'] for m in config['metrics']] + ['Total'],
        'YTD Sep 24': [],
        'Metric Score': [],
        'Weight': [f"{m['weight']}%" for m in config['metrics']] + [f"{config['total_weight']}%"],
        'Weighted Score': []
    }
    
    total_weighted_score = 0
    for metric in config['metrics']:
        try:
            ytd_value = filtered_df[metric['ytd_col']].mean() if metric['ytd_col'] in filtered_df.columns else 0
            score_value = filtered_df[metric['score_col']].mean() if metric['score_col'] in filtered_df.columns else 0
            weighted_score = score_value * (metric['weight'] / 100)
            
            data['YTD Sep 24'].append(f"{ytd_value:.1f}%")
            data['Metric Score'].append(f"{score_value:.1f}%")
            data['Weighted Score'].append(f"{weighted_score:.2f}%")
            
            total_weighted_score += weighted_score
        except:
            data['YTD Sep 24'].append('')
            data['Metric Score'].append('')
            data['Weighted Score'].append('')
    
    data['YTD Sep 24'].append('')
    data['Metric Score'].append('')
    data['Weighted Score'].append(f"{total_weighted_score:.2f}%")
    
    return pd.DataFrame(data)

# Display tables in layout
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="banner"><h6 class="banner-text">Growth & One Chase</h6></div>', unsafe_allow_html=True)
    growth_df = create_metrics_table(filtered_df, 'growth')
    st.dataframe(style_dataframe(growth_df), hide_index=True, use_container_width=True)

    st.markdown('<div class="banner"><h6 class="banner-text">Controls</h6></div>', unsafe_allow_html=True)
    controls_df = create_metrics_table(filtered_df, 'controls')
    st.dataframe(style_dataframe(controls_df), hide_index=True, use_container_width=True)

with col2:
    st.markdown('<div class="banner"><h6 class="banner-text">Customer Experience</h6></div>', unsafe_allow_html=True)
    customer_df = create_metrics_table(filtered_df, 'customer')
    st.dataframe(style_dataframe(customer_df), hide_index=True, use_container_width=True)
    ### Financial Health & Innovation
    st.markdown('<div class="banner"><h6 class="banner-text">Financial Health & Innovation</h6></div>', unsafe_allow_html=True)
    customer_df = create_metrics_table(filtered_df, 'customer')
    st.dataframe(style_dataframe(customer_df), hide_index=True, use_container_width=True)
    ### Culture and Employee
    st.markdown('<div class="banner"><h6 class="banner-text">Culture and Employee</h6></div>', unsafe_allow_html=True)
    financial_df = create_metrics_table(filtered_df, 'financial')
    st.dataframe(style_dataframe(financial_df), hide_index=True, use_container_width=True)
    
st.divider()
