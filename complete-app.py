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

@st.cache_data
def load_data():
    try:
        df = pd.read_excel('scorecard_data_long.xlsx')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load initial data
df = load_data()

if df.empty:
    st.error("No data available. Please check if the data file exists.")
    st.stop()

# Get unique values for filters
scorecard_periods = ['All'] + sorted(df['Scorecard_Period'].unique().tolist())
divisions = ['All'] + sorted(df['Division'].unique().tolist())
regions = ['All'] + sorted(df['Region'].unique().tolist())
markets = ['All Markets'] + sorted(df['Market'].unique().tolist())
branches = ['All'] + sorted(df['Branch_Name'].unique().tolist())

# Filters layout
col1, col2, col3, col4, spacing, col6, col7 = st.columns([1, 1, 1, 1, 0.3, 1, 1])

with col1:
    scorecard_period = st.selectbox("Scorecard Period", scorecard_periods)
with col2:
    division = st.selectbox("Division", divisions)
with col3:
    region = st.selectbox("Region", regions)
with col4:
    market = st.selectbox("Market", markets)
with col6:
    branch = st.selectbox("Branch", branches)
with col7:
    st.button("Export to PDF")

# Filter data based on selections
def filter_data(df):
    mask = pd.Series(True, index=df.index)
    if scorecard_period != 'All':
        mask &= df['Scorecard_Period'] == scorecard_period
    if division != 'All':
        mask &= df['Division'] == division
    if region != 'All':
        mask &= df['Region'] == region
    if market != 'All Markets':
        mask &= df['Market'] == market
    if branch != 'All':
        mask &= df['Branch_Name'] == branch
    return df[mask]


filtered_df = filter_data(df)

if branch != 'All':
    st.info(f"### Branch: {branch}")

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



# First, define all necessary functions
def create_comparison_metric(value):
    """Create HTML for comparison metrics with arrows and colors"""
    try:
        if not value or value == "N/A" or value == "Error":
            return f'<span>N/A</span>'
            
        if isinstance(value, str):
            is_positive = not value.replace('%', '').startswith('-')
        else:
            is_positive = not str(value).startswith('-')
            
        color_class = "positive-value" if is_positive else "negative-value"
        arrow_class = "arrow-up" if is_positive else "arrow-down"
        
        return f'<span class="{color_class} {arrow_class}">{value}</span>'
    except Exception as e:
        st.warning(f"Error formatting comparison metric: {str(e)}")
        return f'<span>N/A</span>'

def calculate_filtered_metrics(filtered_df):
    metrics = {}
    categories = [
        ('Growth & One Chase', '#0052CC'),
        ('Customer Experience', '#00A3BF'),
        ('Financial Health & Innovation', '#36B37E'),
        ('Culture & Employee', '#FF8B00'),
        ('Controls', '#998DD9')
    ]
    
    try:
        if filtered_df.empty:
            return {category: {
                "value": 0.0,
                "color": color,
                "vs_last": "0.0%",
                "peer": "0.0%",
                "national": "0.0%"
            } for category, color in categories}
        
        all_periods = sorted(filtered_df['Scorecard_Period'].unique())
        current_period = all_periods[-1] if all_periods else None
        prev_period = all_periods[-2] if len(all_periods) > 1 else None

        for category, color in categories:
            try:
                category_data = filtered_df[filtered_df['Category'] == category]
                
                if category_data.empty:
                    metrics[category] = {
                        "value": 0.0,
                        "color": color,
                        "vs_last": "0.0%",
                        "peer": "0.0%",
                        "national": "0.0%"
                    }
                    continue

                current_data = category_data[category_data['Scorecard_Period'] == current_period] if current_period else pd.DataFrame()
                current_value = current_data['Value'].mean() if not current_data.empty else 0.0

                prev_data = category_data[category_data['Scorecard_Period'] == prev_period] if prev_period else pd.DataFrame()
                prev_value = prev_data['Value'].mean() if not prev_data.empty else current_value

                peer_group = current_data['Peer_Group'].iloc[0] if not current_data.empty else None
                if peer_group:
                    peer_data = filtered_df[
                        (filtered_df['Category'] == category) & 
                        (filtered_df['Peer_Group'] == peer_group)
                    ]
                    peer_avg = peer_data['Value'].mean() if not peer_data.empty else current_value
                else:
                    peer_avg = current_value

                national_data = filtered_df[filtered_df['Category'] == category]
                national_avg = national_data['Value'].mean() if not national_data.empty else current_value

                vs_last = current_value - prev_value if prev_value is not None else 0.0
                vs_peer = current_value - peer_avg if peer_avg is not None else 0.0
                vs_national = current_value - national_avg if national_avg is not None else 0.0

                metrics[category] = {
                    "value": current_value,
                    "color": color,
                    "vs_last": f"{vs_last:+.1f}%",
                    "peer": f"{vs_peer:+.1f}%",
                    "national": f"{vs_national:+.1f}%"
                }

            except Exception as e:
                st.warning(f"Error calculating metrics for {category}: {str(e)}")
                metrics[category] = {
                    "value": 0.0,
                    "color": color,
                    "vs_last": "N/A",
                    "peer": "N/A",
                    "national": "N/A"
                }

    except Exception as e:
        st.error(f"Error in metric calculations: {str(e)}")
        return {category: {
            "value": 0.0,
            "color": color,
            "vs_last": "Error",
            "peer": "Error",
            "national": "Error"
        } for category, color in categories}

    return metrics

# Calculate metrics after data is loaded and filtered
category_metrics = calculate_filtered_metrics(filtered_df)

# Then display the metrics
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




# Function to create metrics table
def create_metrics_table(filtered_df, category):
    category_data = filtered_df[filtered_df['Category'] == category]
    
    if not category_data.empty:
        metrics_df = pd.DataFrame({
            'Metric': category_data['Subcategory'].unique(),
            'YTD Sep 24': category_data.groupby('Subcategory')['Value'].mean(),
            'Metric Score': category_data.groupby('Subcategory')['Value'].mean(),
            'Weight': category_data.groupby('Subcategory')['Weight'].first(),
            'Weighted Score': category_data.groupby('Subcategory')['Weighted_Score'].mean()
        }).reset_index(drop=True)
        
        # Format the columns
        metrics_df['YTD Sep 24'] = metrics_df['YTD Sep 24'].round(1).astype(str) + '%'
        metrics_df['Metric Score'] = metrics_df['Metric Score'].round(1).astype(str) + '%'
        metrics_df['Weight'] = metrics_df['Weight'].astype(str) + '%'
        metrics_df['Weighted Score'] = metrics_df['Weighted Score'].round(2).astype(str) + '%'
        
        return metrics_df
    return pd.DataFrame()

# Display category tables
categories = [
    'Growth & One Chase',
    'Customer Experience',
    'Financial Health & Innovation',
    'Culture & Employee',
    'Controls'
]

st.divider()

# Display tables in rows
for i in range(0, len(categories), 2):
    col1, col2 = st.columns(2)
    
    with col1:
        if i < len(categories):
            st.subheader(categories[i])
            metrics_df = create_metrics_table(filtered_df, categories[i])
            if not metrics_df.empty:
                st.dataframe(
                    metrics_df,
                    hide_index=True,
                    use_container_width=True
                )
    
    with col2:
        if i + 1 < len(categories):
            st.subheader(categories[i + 1])
            metrics_df = create_metrics_table(filtered_df, categories[i + 1])
            if not metrics_df.empty:
                st.dataframe(
                    metrics_df,
                    hide_index=True,
                    use_container_width=True
                )

# Display last table if odd number of categories
if len(categories) % 2 != 0:
    st.subheader(categories[-1])
    metrics_df = create_metrics_table(filtered_df, categories[-1])
    if not metrics_df.empty:
        st.dataframe(
            metrics_df,
            hide_index=True,
            use_container_width=True
        )

# Detailed metrics tables
col1, col2 = st.columns(2)

# Growth & One Chase table
with col1:
    metrics = get_subcategory_metrics(filtered_df, "Growth & One Chase")
    metrics_html = "".join([f"""
                <tr>
                    <td>{m['Metric']}</td>
                    <td>{m['YTD Sep 24']}</td>
                    <td>{m['Metric Score']}</td>
                    <td>{m['Weight']}</td>
                    <td>{m['Weighted Score']}</td>
                </tr>
    """ for m in metrics])
    
    st.markdown(f"""
    <div class="metric-box">
        <div class="table-header"><h6>Growth & One Chase</h6></div>
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
                {metrics_html}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Customer Experience table
with col2:
    metrics = get_subcategory_metrics(filtered_df, "Customer Experience")
    metrics_html = "".join([f"""
                <tr>
                    <td>{m['Metric']}</td>
                    <td>{m['YTD Sep 24']}</td>
                    <td>{m['Metric Score']}</td>
                    <td>{m['Weight']}</td>
                    <td>{m['Weighted Score']}</td>
                </tr>
    """ for m in metrics])
    
    st.markdown(f"""
    <div class="metric-box">
        <div class="table-header"><h6>Customer Experience</h6></div>
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
                {metrics_html}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Second row of tables
col3, col4 = st.columns(2)
 
with col3:
    metrics = get_subcategory_metrics(filtered_df, "Financial Health & Innovation")
    metrics_html = "".join([f"""
                <tr>
                    <td>{m['Metric']}</td>
                    <td>{m['YTD Sep 24']}</td>
                    <td>{m['Metric Score']}</td>
                    <td>{m['Weight']}</td>
                    <td>{m['Weighted Score']}</td>
                </tr>
    """ for m in metrics])
    
    st.markdown(f"""
    <div class="metric-box">
        <div class="table-header"><h6>Financial Health & Innovation</h6></div>
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
                {metrics_html}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col4:
    metrics = get_subcategory_metrics(filtered_df, "Culture & Employee")
    metrics_html = "".join([f"""
                <tr>
                    <td>{m['Metric']}</td>
                    <td>{m['YTD Sep 24']}</td>
                    <td>{m['Metric Score']}</td>
                    <td>{m['Weight']}</td>
                    <td>{m['Weighted Score']}</td>
                </tr>
    """ for m in metrics])
    
    st.markdown(f"""
    <div class="metric-box">
        <div class="table-header"><h6>Culture & Employee</h6></div>
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
                {metrics_html}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    metrics = get_subcategory_metrics(filtered_df, "Controls")
    metrics_html = "".join([f"""
                <tr>
                    <td>{m['Metric']}</td>
                    <td>{m['YTD Sep 24']}</td>
                    <td>{m['Metric Score']}</td>
                    <td>{m['Weight']}</td>
                    <td>{m['Weighted Score']}</td>
                </tr>
    """ for m in metrics])
    
    st.markdown(f"""
    <div class="metric-box">
        <div class="table-header"><h6>Controls</h6></div>
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
                {metrics_html}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)