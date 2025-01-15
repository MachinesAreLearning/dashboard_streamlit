import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_long_format_data(num_branches=100, months_of_data=12):
    # Fixed category mappings
    category_subcategory_mapping = {
        'Growth & One Chase': [
            'Total DDA Balance Growth',
            'Net Checking Acquisition',
            'Banker Coverage of Calls/Meeting Guidance',
            'Discover Needs at New Account Opening',
            'First Time Investors Ratio',
            'Loan Originations',
            'Credit Card Activations Ratio'
        ],
        'Customer Experience': [
            'Branch OSAT',
            'Customer Satisfaction',
            'Wait Time',
            'Resolution Rate'
        ],
        'Financial Health & Innovation': [
            'Digital Adoption',
            'Financial Health Conversations',
            'Innovation Projects',
            'Process Efficiency'
        ],
        'Culture & Employee': [
            'Employee Engagement',
            'Training Completion',
            'Leadership Score',
            'Turnover Rate'
        ],
        'Controls': [
            'Audit Score',
            'Compliance Rating',
            'Risk Assessment',
            'Security Measures'
        ]
    }

    # Base data lists
    divisions = ['Midwest', 'Northeast', 'South', 'West']
    regions = {
        'Midwest': ['Ohio', 'Michigan', 'Illinois', 'Indiana'],
        'Northeast': ['New York', 'Massachusetts', 'Pennsylvania'],
        'South': ['Florida', 'Texas', 'Georgia'],
        'West': ['California', 'Washington', 'Oregon']
    }
    markets = ['Urban', 'Suburban', 'Rural']
    performance_tiers = ['PL1', 'PL2', 'PL3', 'PL4', 'PL5', 'PL6']

    # Generate base branch data
    branches = []
    for i in range(num_branches):
        division = np.random.choice(divisions)
        region = np.random.choice(regions[division])
        branch = {
            'Branch_ID': f'BR{i:04d}',
            'Branch_Name': f'Branch {i:04d}',
            'Division': division,
            'Region': region,
            'Market': np.random.choice(markets),
            'Peer_Group': f'Group {i % 10 + 1}',
            'Country': 'USA',
            'Branch_Manager_SID': f'SID{i:05d}',
            'Branch_Manager_Name': f'Manager {i:04d}',
            'Tenure': np.random.randint(1, 20)
        }
        branches.append(branch)

    # Generate time series data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30*months_of_data)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')

    # Create long format data
    data = []
    for date in dates:
        month = date.strftime('%B')
        year = date.year
        scorecard_period = f"{month} {year}"
        
        for branch in branches:
            base_weighted_score = np.random.normal(75, 15)  # Base score around 75%
            
            for category, subcategories in category_subcategory_mapping.items():
                category_score = max(0, min(100, base_weighted_score + np.random.normal(0, 5)))
                
                for subcategory in subcategories:
                    row = {
                        'Month': month,
                        'Year': year,
                        'Scorecard_Period': scorecard_period,
                        'Division': branch['Division'],
                        'Region': branch['Region'],
                        'Market': branch['Market'],
                        'Branch_ID': branch['Branch_ID'],
                        'Branch_Name': branch['Branch_Name'],
                        'Peer_Group': branch['Peer_Group'],
                        'Country': branch['Country'],
                        'Branch_Manager_SID': branch['Branch_Manager_SID'],
                        'Branch_Manager_Name': branch['Branch_Manager_Name'],
                        'Tenure': branch['Tenure'],
                        'Overall_Weighted_Score': base_weighted_score,
                        'Peer_Group_Member_Count': np.random.randint(50, 150),
                        'Performance_Tier': np.random.choice(performance_tiers),
                        'Category': category,
                        'Subcategory': subcategory,
                        'Drill_Down_Subcategory': f'{subcategory} Detail',
                        'Market_Chart_Sort_Order': np.random.randint(1, 100),
                        'Market_Chart_Indicator': np.random.choice(['↑', '→', '↓']),
                        'Value': max(0, min(100, category_score + np.random.normal(0, 2))),
                        'Value_Type': 'Percentage',
                        'Perspective': np.random.choice(['Financial', 'Customer', 'Process', 'People']),
                        'Data_Refresh_Date': datetime.now().strftime('%Y-%m-%d')
                    }
                    data.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Calculate some metrics based on hierarchy
    df['Value'] = df.groupby(['Scorecard_Period', 'Branch_ID', 'Category'])['Value'].transform(
        lambda x: x + np.random.normal(0, 1))  # Add some noise to values

    # Save to Excel
    df.to_excel('scorecard_data_long.xlsx', index=False)
    print(f"Generated {len(df)} records in long format")
    return df

if __name__ == "__main__":
    # Generate data for 100 branches over 12 months
    df = generate_long_format_data(num_branches=100, months_of_data=12)
    print("Data has been saved to 'scorecard_data_long.xlsx'")
    
    # Print some sample statistics
    print("\nSample Statistics:")
    print(f"Total number of records: {len(df)}")
    print("\nUnique counts:")
    for col in ['Division', 'Region', 'Market', 'Category', 'Subcategory']:
        print(f"{col}: {df[col].nunique()}")
    
    print("\nValue statistics:")
    print(df['Value'].describe())