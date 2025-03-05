import streamlit as st
import pandas as pd
import numpy as np
from styles import get_dashboard_styles, get_table_styles, apply_default_styles
from utils import (create_metric_box, create_metric_box_0, create_comparison_metric, 
                  calculate_comparison, style_dataframe)
from config import METRICS_CONFIG, TABLE_CONFIGS
from comparison_utils import (load_data_versions, create_comparison_indicator, format_with_delta,
                            calculate_impact, create_impact_table, style_impact_table)
from data_comparison import (load_comparison_data, filter_comparison_data, calculate_change,
                           find_top_impacts, generate_impact_summary, highlight_changes,
                           create_comparison_view, generate_explanation)

# Set page configuration
st.set_page_config(layout="wide", page_title="Branch Manager Scorecard", page_icon="📊")

# Apply styles
st.markdown(apply_default_styles(), unsafe_allow_html=True)

# Add custom CSS for delta indicators
st.markdown("""
<style>
    .delta-indicator {
        display: inline-block;
        margin-left: 5px;
        font-size: 0.85em;
    }
    .positive-delta {
        color: #40c057;
    }
    .negative-delta {
        color: #fa5252;
    }
    .neutral-delta {
        color: #adb5bd;
    }
    .previous-value {
        text-decoration: line-through;
        color: #adb5bd;
        font-size: 0.85em;
    }
    .comparison-info {
        background-color: #f0f7ff;
        border-left: 4px solid #0052CC;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 0 4px 4px 0;
    }
    .impact-summary {
        margin-top: 20px;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #e9ecef;
    }
    .impact-item {
        margin-bottom: 8px;
        padding-left: 10px;
        border-left: 3px solid #0052CC;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="blue-header"><h3>Consumer Banking Branch Manager Scorecard</h3></div>', unsafe_allow_html=True)

# Region selector with spacing
col1, col2, col3, col4, spacing, col5, spacing, col6 = st.columns([1, 1, 1, 1, 0.3, 1, 2.5, 1])

# Debug comparison checkbox
with col6:
    debug_compare = st.checkbox("Debug: Compare with Previous", key="debug_compare")

# Checkbox for actual data
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

# Load comparison data if debug mode is enabled
if debug_compare:
    try:
        current_df = pd.read_csv('branch_data.csv')
        previous_df = pd.read_csv('branch_data_previous.csv')
    except Exception as e:
        st.error(f"Error loading comparison data: {str(e)}")
        st.warning("Make sure you have both branch_data.csv and branch_data_previous.csv files.")
        debug_compare = False
        current_df, previous_df = None, None
else:
    current_df, previous_df = None, None

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

# Get filtered comparison data if debug mode is enabled
if debug_compare and current_df is not None and previous_df is not None:
    filtered_current_df = current_df.copy()
    filtered_previous_df = previous_df.copy()
    
    # Apply filters to comparison data
    if division != 'All Divisions':
        filtered_current_df = filtered_current_df[filtered_current_df['Division'] == division]
        if 'Division' in filtered_previous_df.columns:
            filtered_previous_df = filtered_previous_df[filtered_previous_df['Division'] == division]
    if region != 'All Regions':
        filtered_current_df = filtered_current_df[filtered_current_df['Region'] == region]
        if 'Region' in filtered_previous_df.columns:
            filtered_previous_df = filtered_previous_df[filtered_previous_df['Region'] == region]
    if market != 'All Markets':
        filtered_current_df = filtered_current_df[filtered_current_df['Market'] == market]
        if 'Market' in filtered_previous_df.columns:
            filtered_previous_df = filtered_previous_df[filtered_previous_df['Market'] == market]
    if branch != 'All Branches':
        filtered_current_df = filtered_current_df[filtered_current_df['Branch'] == branch]
        if 'Branch' in filtered_previous_df.columns:
            filtered_previous_df = filtered_previous_df[filtered_previous_df['Branch'] == branch]
else:
    filtered_current_df = None
    filtered_previous_df = None

# Display comparison info if debug mode is enabled
if debug_compare:
    st.markdown("""
    <div class="comparison-info">
        <h4>Debug Comparison Mode</h4>
        <p>Showing changes between previous and current scorecard data.</p>
        <p>Format: <strong>Current Value</strong> (<span class="previous-value">Previous Value</span> → <span class="positive-delta">+Change</span> or <span class="negative-delta">-Change</span>)</p>
    </div>
    """, unsafe_allow_html=True)

# Function to create delta indicator HTML
def create_delta_indicator(current_value, previous_value, format_as_percent=True):
    """Create HTML for delta indicator (e.g., 1.7% → 1.9%, +0.2%)"""
    if pd.isna(current_value) or pd.isna(previous_value):
        return current_value if not pd.isna(current_value) else ""
    
    delta = current_value - previous_value
    
    # Format values
    if format_as_percent:
        current_str = f"{current_value:.1f}%"
        previous_str = f"{previous_value:.1f}%"
        delta_str = f"{delta:+.1f}%"
    else:
        current_str = f"{current_value}"
        previous_str = f"{previous_value}"
        delta_str = f"{delta:+}"
    
    # Determine delta class
    delta_class = "positive-delta" if delta > 0 else ("negative-delta" if delta < 0 else "neutral-delta")
    
    # Create HTML
    html = f"""
    {current_str} <br><small>(<span class="previous-value">{previous_str}</span> → <span class="{delta_class}">{delta_str}</span>)</small>
    """
    
    return html

# Calculate PL distribution
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
    if debug_compare and filtered_current_df is not None and filtered_previous_df is not None:
        try:
            current_score = filtered_current_df['gofirsttime-wt'].mean()
            previous_score = filtered_previous_df['gofirsttime-wt'].mean() if 'gofirsttime-wt' in filtered_previous_df.columns else 0
            delta = current_score - previous_score
            delta_class = "positive-delta" if delta >= 0 else "negative-delta"
            
            delta_display = f"<br><small>(<span class='previous-value'>{previous_score:.2f}%</span> → <span class='{delta_class}'>{delta:+.2f}%</span>)</small>"
            st.markdown(create_metric_box("Overall Weighted Score", f"{current_score:.2f}%{delta_display}"), unsafe_allow_html=True)
        except Exception as e:
            overall_score = filtered_df['gofirsttime-wt'].mean()
            st.markdown(create_metric_box("Overall Weighted Score", f"{overall_score:.2f}%"), unsafe_allow_html=True)
    else:
        overall_score = filtered_df['gofirsttime-wt'].mean()
        st.markdown(create_metric_box("Overall Weighted Score", f"{overall_score:.2f}%"), unsafe_allow_html=True)

with col2:
    if debug_compare and filtered_current_df is not None and filtered_previous_df is not None:
        try:
            current_rank = filtered_current_df['overall_rank'].iloc[0] if not filtered_current_df.empty else "N/A"
            previous_rank = filtered_previous_df['overall_rank'].iloc[0] if not filtered_previous_df.empty and 'overall_rank' in filtered_previous_df.columns else "N/A"
            
            if current_rank != "N/A" and previous_rank != "N/A":
                current_rank = int(current_rank)
                previous_rank = int(previous_rank)
                delta_rank = current_rank - previous_rank
                delta_class = "positive-delta" if delta_rank <= 0 else "negative-delta"
                
                delta_display = f"<br><small>(<span class='previous-value'>{previous_rank}</span> → <span class='{delta_class}'>{delta_rank:+}</span>)</small>"
            else:
                delta_display = ""
            
            st.markdown(create_metric_box("Overall Rank", f"{current_rank}{delta_display}"), unsafe_allow_html=True)
        except Exception as e:
            rank = filtered_df['overall_rank'].iloc[0] if not filtered_df.empty else "N/A"
            st.markdown(create_metric_box("Overall Rank", rank), unsafe_allow_html=True)
    else:
        rank = filtered_df['overall_rank'].iloc[0] if not filtered_df.empty else "N/A"
        st.markdown(create_metric_box("Overall Rank", rank), unsafe_allow_html=True)

with col3:
    if debug_compare and filtered_current_df is not None and filtered_previous_df is not None:
        try:
            # Calculate for previous data
            total_branches_prev = len(filtered_previous_df)
            if total_branches_prev > 0 and 'Performance_Level' in filtered_previous_df.columns:
                pl_12_count_prev = len(filtered_previous_df[filtered_previous_df['Performance_Level'].isin([1, 2])])
                pl_56_count_prev = len(filtered_previous_df[filtered_previous_df['Performance_Level'].isin([5, 6])])
                
                pl_12_pct_prev = (pl_12_count_prev / total_branches_prev) * 100
                pl_56_pct_prev = (pl_56_count_prev / total_branches_prev) * 100
            else:
                pl_12_pct_prev = 0
                pl_56_pct_prev = 0
                
            # Calculate for current data
            total_branches_curr = len(filtered_current_df)
            if total_branches_curr > 0:
                pl_12_count_curr = len(filtered_current_df[filtered_current_df['Performance_Level'].isin([1, 2])])
                pl_56_count_curr = len(filtered_current_df[filtered_current_df['Performance_Level'].isin([5, 6])])
                
                pl_12_pct_curr = (pl_12_count_curr / total_branches_curr) * 100
                pl_56_pct_curr = (pl_56_count_curr / total_branches_curr) * 100
            else:
                pl_12_pct_curr = 0
                pl_56_pct_curr = 0
                
            pl_12_delta = pl_12_pct_curr - pl_12_pct_prev
            pl_56_delta = pl_56_pct_curr - pl_56_pct_prev
            
            pl_12_delta_class = "positive-delta" if pl_12_delta >= 0 else "negative-delta"
            pl_56_delta_class = "positive-delta" if pl_56_delta >= 0 else "negative-delta"
            
            pl_display = f"{pl_12_pct_curr:.1f}% / {pl_56_pct_curr:.1f}% <br><small>(<span class='previous-value'>{pl_12_pct_prev:.1f}% / {pl_56_pct_prev:.1f}%</span> → <span class='{pl_12_delta_class}'>{pl_12_delta:+.1f}%</span> / <span class='{pl_56_delta_class}'>{pl_56_delta:+.1f}%</span>)</small>"
            
            st.markdown(create_metric_box_0("% of Branches in PL 1/2 vs. PL 5/6", pl_display), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in PL calculation: {str(e)}")
            pl_dist = calculate_pl_distribution(filtered_df)
            st.markdown(create_metric_box_0("% of Branches in PL 1/2 vs. PL 5/6", pl_dist), unsafe_allow_html=True)
    else:
        pl_dist = calculate_pl_distribution(filtered_df)
        st.markdown(create_metric_box_0("% of Branches in PL 1/2 vs. PL 5/6", pl_dist), unsafe_allow_html=True)

# Display performance metrics with comparison data if debug mode is enabled
col1, col2, col3, col4, col5 = st.columns(5)
columns = [col1, col2, col3, col4, col5]

for i, (metric, config) in enumerate(METRICS_CONFIG.items()):
    with columns[i]:
        if debug_compare and filtered_current_df is not None and filtered_previous_df is not None:
            try:
                current_value = filtered_current_df[config['score_column']].mean() if config['score_column'] in filtered_current_df.columns else 0
                previous_value = filtered_previous_df[config['score_column']].mean() if config['score_column'] in filtered_previous_df.columns else 0
                
                delta = current_value - previous_value
                delta_text = f"{delta:+.2f}%"
                delta_class = "positive-delta" if delta >= 0 else "negative-delta"
                
                fill_percentage = min((current_value / config['max_value']) * 100, 100)
                
                comparison_html = f"""
                <div class="metric-percentage">{current_value:.2f}% <br><small>(<span class="previous-value">{previous_value:.2f}%</span> → <span class="{delta_class}">{delta_text}</span>)</small></div>
                """
                
                # Calculate comparison values
                comparisons = {
                    key: calculate_comparison(filtered_current_df, col) 
                    for key, col in config['comparison_columns'].items()
                }
            except Exception as e:
                value = filtered_df[config['score_column']].mean() if config['score_column'] in filtered_df.columns else 0
                fill_percentage = min((value / config['max_value']) * 100, 100)
                
                comparisons = {
                    key: calculate_comparison(filtered_df, col) 
                    for key, col in config['comparison_columns'].items()
                }
                
                comparison_html = f"""
                <div class="metric-percentage">{value:.2f}%</div>
                """
        else:
            value = filtered_df[config['score_column']].mean() if config['score_column'] in filtered_df.columns else 0
            fill_percentage = min((value / config['max_value']) * 100, 100)
            
            comparisons = {
                key: calculate_comparison(filtered_df, col) 
                for key, col in config['comparison_columns'].items()
            }
            
            comparison_html = f"""
            <div class="metric-percentage">{value:.2f}%</div>
            """
        
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title" style="font-weight: 600;">{metric}</div>
            {comparison_html}
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


# # Display impact analysis if debug mode is enabled
if debug_compare and filtered_current_df is not None and filtered_previous_df is not None:
    # Create tabs for impact analysis
    st.markdown("## Impact Analysis")
    st.markdown("This analysis shows how changes in each metric contribute to the overall scorecard changes.")
    
    try:
        impact_tabs = st.tabs(["Growth & One Chase", "Customer Experience", "Financial Health & Innovation", "Controls"])
        
        # Store impact tables for summary
        impact_tables = {}
        
        with impact_tabs[0]:
            growth_impact = create_impact_table(filtered_current_df, filtered_previous_df, 'growth', TABLE_CONFIGS['growth'])
            st.dataframe(style_impact_table(growth_impact), hide_index=True, use_container_width=True)
            impact_tables['Growth'] = growth_impact
        
        with impact_tabs[1]:
            customer_impact = create_impact_table(filtered_current_df, filtered_previous_df, 'customer', TABLE_CONFIGS['customer'])
            st.dataframe(style_impact_table(customer_impact), hide_index=True, use_container_width=True)
            impact_tables['Customer'] = customer_impact
        
        with impact_tabs[2]:
            financial_impact = create_impact_table(filtered_current_df, filtered_previous_df, 'financial', TABLE_CONFIGS['financial'])
            st.dataframe(style_impact_table(financial_impact), hide_index=True, use_container_width=True)
            impact_tables['Financial'] = financial_impact
        
        with impact_tabs[3]:
            controls_impact = create_impact_table(filtered_current_df, filtered_previous_df, 'controls', TABLE_CONFIGS['controls'])
            st.dataframe(style_impact_table(controls_impact), hide_index=True, use_container_width=True)
            impact_tables['Controls'] = controls_impact
        
        # Create impact summary
        top_positive, top_negative = generate_impact_summary(impact_tables)
        
        if not top_positive.empty or not top_negative.empty:
            st.markdown("""
            <div class="comparison-summary">
                <h4>Summary of Key Changes</h4>
            """, unsafe_allow_html=True)
            
            if not top_positive.empty:
                st.markdown("<p>Biggest positive impacts:</p>", unsafe_allow_html=True)
                for _, row in top_positive.iterrows():
                    st.markdown(f"""
                    <div class="top-impact-item top-impact-positive">
                        <strong>{row['Metric']}</strong> ({row['Category']}): {row['Impact']} to overall score
                    </div>
                    """, unsafe_allow_html=True)
            
            if not top_negative.empty:
                st.markdown("<p>Biggest negative impacts:</p>", unsafe_allow_html=True)
                for _, row in top_negative.iterrows():
                    st.markdown(f"""
                    <div class="top-impact-item top-impact-negative">
                        <strong>{row['Metric']}</strong> ({row['Category']}): {row['Impact']} to overall score
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error in impact analysis: {str(e)}")
    
    st.divider()
