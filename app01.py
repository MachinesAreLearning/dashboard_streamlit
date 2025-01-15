import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(layout="wide")

# Custom CSS styling
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    .blue-header {
        background-color: #0052CC;
        color: white;
        padding: 15px;
        border-radius: 3px 3px 0 0;
        margin-bottom: 20px;
    }
    .blue-header h3 {
        color: white !important;
        margin: 0;
        font-size: 20px;
    }
    .metric-container {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 5px;
        height: 120px;
        position: relative;
        margin-bottom: 20px;
    }
    .metric-label {
        font-size: 36px;
        color: #333;
        position: absolute;
        bottom: 20px;
        left: 20px;
        font-weight: 500;
    }
     .metric-label-2 {
        font-size: 24px;
        color: #333;
        position: absolute;
        bottom: 70px;
        left: 20px;
        font-weight: 500;
        width: 60%;
        line-height: 1.4;
    }
    .metric-value {
        font-size: 40px;
        font-weight: bold;
        color: #333;
        position: absolute;
        bottom: 20px;
        right: 20px;
    }
    .ytd-label-top {
        position: absolute;
        top: 10px;
        right: 20px;
        color: #666;
        font-size: 18px;
    }
    .metric-box {
        background-color: white;
        padding: 15px 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 14px;
        color: #333;
        margin-bottom: 8px;
    }
    .metric-percentage {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
    }
    .progress-container {
        height: 8px;
        background-color: #E0E0E0;
        border-radius: 10px;
        margin: 8px 0;
        position: relative;
    }
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        position: absolute;
        left: 0;
    }
    .comparison-labels {
        display: flex;
        justify-content: space-between;
        color: #666;
        font-size: 12px;
        margin-bottom: 5px;
    }
    .comparison-values {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
    }
    .positive-value {
        color: #36B37E;
    }
    .negative-value {
        color: #FF5630;
    }
    .arrow-up::before {
        content: "↑";
        margin-right: 2px;
    }
    .arrow-down::before {
        content: "↓";
        margin-right: 2px;
    }
    .metric-tables {
        margin-top: 30px;
    }
    .table-header {
        font-size: 16px;
        color: #333;
        margin-bottom: 15px;
        font-weight: 500;
    }
    .metric-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 13px;
    }
    .metric-table th {
        background-color: #f5f5f5;
        padding: 10px;
        text-align: left;
        border: 1px solid #ddd;
        font-weight: 500;
    }
    .metric-table td {
        padding: 8px 10px;
        border: 1px solid #ddd;
        background-color: white;
    }
    .metric-table td:not(:first-child) {
        text-align: right;
    }
    .metric-table tr:hover td {
        background-color: #f8f9fa;
    }
    .metric-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .metric-title {
        font-size: 14px;
        color: #333;
    }
    .metric-percentage {
        font-size: 16px;
        font-weight: 600;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="blue-header"><h3>Consumer Banking Branch Manager Scorecard</h3></div>', unsafe_allow_html=True)

# Region selector with spacing
col1, col2, col3, spacing,col4,spacing, col5 = st.columns([1, 1, 1,0.3, 1, 2.5, 1])
with col1:
    division = st.selectbox("Division", ["Midwest"])
with col2:
    region = st.selectbox("Region", ["Ohio"])
with col3:
    market = st.selectbox("Market", ["All Markets"])
with col4:
    st.checkbox("save as default", key="disabled")
with col5:
    st.button("Export to PDF")

# Main metrics
def create_metric_box(label, value):
    return f"""
    <div class="metric-container">
        <div class="ytd-label-top">YTD</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """
def create_metric_box_0(label, value):
    return f"""
    <div class="metric-container">
        <div class="ytd-label-top">YTD</div>
        <div class="metric-label-2">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(create_metric_box("Overall Weighted Score", "76.07%"), unsafe_allow_html=True)
with col2:
    st.markdown(create_metric_box("Overall Rank", "4"), unsafe_allow_html=True)
with col3:
    st.markdown(create_metric_box_0("% of Branches in PL 1/2 vs. PL 5/6", "45.8% / 19.3%"), unsafe_allow_html=True)

# Performance metric boxes
def create_comparison_metric(value):
    is_positive = not value.startswith('-')
    color_class = "positive-value" if is_positive else "negative-value"
    arrow_class = "arrow-up" if is_positive else "arrow-down"
    return f'<span class="{color_class} {arrow_class}">{value}</span>'

metrics_data = {
    "Growth & One Chase": {
        "value": 43.21,
        "color": "#0052CC",
        "vs_last": "-2.0%",
        "peer": "+1.0%",
        "national": "+2.0%"
    },
    "Customer Experience": {
        "value": 13.21,
        "color": "#00A3BF",
        "vs_last": "+2.0%",
        "peer": "+1.0%",
        "national": "+2.0%"
    },
    "Financial Health & Innovation": {
        "value": 5.38,
        "color": "#36B37E",
        "vs_last": "-2.0%",
        "peer": "+1.0%",
        "national": "+2.0%"
    },
    "Culture & Employee": {
        "value": 14.94,
        "color": "#FF8B00",
        "vs_last": "+1.0%",
        "peer": "+1.0%",
        "national": "+2.0%"
    },
    "Controls": {
        "value": 0.67,
        "color": "#998DD9",
        "vs_last": "-2.0%",
        "peer": "-1.0%",
        "national": "+2.0%"
    }
}

col1, col2, col3, col4, col5 = st.columns(5)
columns = [col1, col2, col3, col4, col5]

for i, (metric, data) in enumerate(metrics_data.items()):
    with columns[i]:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-header-row">
                <div class="metric-title">{metric}</div>
                <div class="metric-percentage">{data['value']}%</div>
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
# Detailed metrics tables
col1, col2 = st.columns(2)

# Growth & One Chase table
with col1:
    st.markdown("""
    <div class="metric-box">
        <div class="table-header"><h6>Growth & One Chase<h6></div>
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
                <tr>
                    <td>Total DDA Balance Growth</td>
                    <td>0.6%</td>
                    <td>43.1%</td>
                    <td>15.0%</td>
                    <td>6.47%</td>
                </tr>
                <tr>
                    <td>Net Checking Acquisition</td>
                    <td>7.1%</td>
                    <td>94.1%</td>
                    <td>7.5%</td>
                    <td>7.06%</td>
                </tr>
                <tr>
                    <td>Banker Coverage of Calls/Meeting Guidance</td>
                    <td>100.0%</td>
                    <td>100.0%</td>
                    <td>5.0%</td>
                    <td>5.0%</td>
                </tr>
                <tr>
                    <td>Discover Needs at New Account Opening</td>
                    <td>96.9%</td>
                    <td>100.0%</td>
                    <td>5.0%</td>
                    <td>5.0%</td>
                </tr>
                <tr>
                    <td>First Time Investors Ratio</td>
                    <td>40.6%</td>
                    <td>96.1%</td>
                    <td>10.0%</td>
                    <td>9.61%</td>
                </tr>
                <tr>
                    <td>Loan Originations</td>
                    <td>15.9%</td>
                    <td>76.5%</td>
                    <td>7.5%</td>
                    <td>5.74%</td>
                </tr>
                <tr>
                    <td>Credit Card Activations Ratio</td>
                    <td>106.2%</td>
                    <td>23.5%</td>
                    <td>10.0%</td>
                    <td>2.35%</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Customer Experience table

with col2:
    st.markdown("""
    <div class="metric-box">
    <div class="table-header"><h6>Customer Experience<h6></div>
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
                <tr>
                    <td>Branch OSAT</td>
                    <td>91.1%</td>
                    <td>91.1%</td>
                    <td>15.0%</td>
                    <td>13.66%</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Detailed metrics tables
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
        <div class="metric-box">
        <div class="table-header"><h6>Financial Health & Innovation<h6></div>
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
                <tr>
                    <td>Branch OSAT</td>
                    <td>91.1%</td>
                    <td>91.1%</td>
                    <td>15.0%</td>
                    <td>13.66%</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Customer Experience table
with col4:
    st.markdown("""
        <div class="metric-box">
        <div class="table-header"><h6>Culture & Employee<h6></div>
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
                <tr>
                    <td>Branch OSAT</td>
                    <td>91.1%</td>
                    <td>91.1%</td>
                    <td>15.0%</td>
                    <td>13.66%</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)



col5, col6 = st.columns(2)

# Customer Experience table
with col5:
    st.markdown("""
        <div class="metric-box">
        <div class="table-header"><h6>Controls<h6></div>
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
                <tr>
                    <td>Branch OSAT</td>
                    <td>91.1%</td>
                    <td>91.1%</td>
                    <td>15.0%</td>
                    <td>13.66%</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)