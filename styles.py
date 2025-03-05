# styles.py

def get_dashboard_styles():
    return """
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
            color: #666;
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
            color: #40c057;
        }
        .negative-value {
            color: #fa5252;
        }
        .arrow-up::before {
            content: "↑";
            margin-right: 2px;
        }
        .arrow-down::before {
            content: "↓";
            margin-right: 2px;
        }
        .stDivider {
            margin: 24px 0;
            border-color: #e9ecef;
        }
        /* Selection box styling */
        div[data-baseweb="select"] > div {
            background-color: white;
            border-color: #ddd;
        }
        /* Button styling */
        .stButton > button {
            background-color: white;
            color: #666;
            border: 1px solid #ddd;
        .metric-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            height: 120px;
            position: relative;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .metric-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        }
        
        .metric-box {
            background-color: white;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .metric-box:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
        }
        
        .banner {
            background: rgb(24, 90, 219);
            padding: 506px 10px;
            border-radius: 16px 18px 0 0;
            margin-bottom: 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        
        .banner:hover {
            transform: translateY(-2px);
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 10px;
            position: absolute;
            left: 0;
            transition: width 0.6s ease, background-color 0.3s ease;
        }
        
        .stDataFrame {
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .stDataFrame:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        /* Add glowing effect to positive/negative values */
        .positive-value {
            color: #40c057;
            text-shadow: 0 0 10px rgba(64, 192, 87, 0.2);
            transition: text-shadow 0.3s;
        }
        
        .negative-value {
            color: #fa5252;
            text-shadow: 0 0 10px rgba(250, 82, 82, 0.2);
            transition: text-shadow 0.3s;
        }
        
        .positive-value:hover, .negative-value:hover {
            text-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
        }        
        
    </style>
    """

def get_table_styles():
    return """
    <style>
        /* Banner styling */
        .banner {
            background: rgb(24, 90, 219);
            padding: 6px 10px;
            border-radius: 16px 18px 0 0;
            margin-bottom: 0;
        }
        .banner-text {
            color: white;
            margin: 0;
            font-size: 26px;
            font-weight: 500;
        }
        
        /* DataFrame styling */
        [data-testid="stDataFrame"] {
            width: 100%;
        }
        .dataframe {
            width: 100%;
            border-collapse: collapse;
        }
        .dataframe th {
            background-color: #f8f9fa;
            color: #666;
            font-weight: 400;
            text-align: left;
            padding: 8px 16px;
            border-bottom: 2px solid #e6e6e6;
        }
        .dataframe td {
            padding: 8px 16px;
            border-bottom: 1px solid #e6e6e6;
        }
        .dataframe tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        /* Metric column styling */
        .dataframe td:first-child {
            text-align: left;
            font-weight: 500;
            color: #0052CC;
            border-right: 2px solid #f0f0f0;
        }
        
        /* Number column styling */
        .dataframe td:not(:first-child) {
            text-align: right;
        }
        
        /* Total row styling */
        .dataframe tr:last-child {
            background-color: #f9f9f9;
            font-weight: 700;
            border-top: 2px solid #e6e6e6;
        }
    </style>
    """

def apply_default_styles():
    return get_dashboard_styles() + get_table_styles()