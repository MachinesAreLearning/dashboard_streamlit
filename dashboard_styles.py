# dashboard_styles.py

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
        .metric-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 13px;
            margin-top: 10px;
        }
        .metric-table th {
            background-color: #f5f5f5;
            padding: 12px 15px;
            text-align: left;
            border: 1px solid #ddd;
            font-weight: 500;
            color: #333;
        }
        .metric-table td {
            padding: 10px 15px;
            border: 1px solid #ddd;
            background-color: white;
            vertical-align: middle;
        }
        .metric-table td:not(:first-child) {
            text-align: right;
        }
        .metric-table tr:hover td {
            background-color: #f8f9fa;
        }
        .table-header h6 {
            font-size: 16px;
            font-weight: 500;
            color: #333;
            margin: 0;
            padding: 0;
        }
    </style>
    """