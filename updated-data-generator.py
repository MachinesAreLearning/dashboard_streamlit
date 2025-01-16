import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

def generate_sid():
    letter = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(string.digits, k=6))
    return f"{letter}{numbers}"

def determine_performance_tier(score):
    if score >= 90:
        return 'PL1'
    elif score >= 80:
        return 'PL2'
    elif score >= 70:
        return 'PL3'
    elif score >= 60:
        return 'PL4'
    elif score >= 50:
        return 'PL5'
    else:
        return 'PL6'

def generate_chase_scorecard_data(start_date='2024-06-01', end_date='2024-09-30'):
    # Chase branches data with pre-assigned SIDs
    chase_branches = {
        'Ohio': [
            {'name': 'Chase Bank Cleveland Downtown', 'id': 'BR1001', 'peer': 'Urban Core', 'sid': generate_sid()},
            {'name': 'Chase Bank Columbus State St', 'id': 'BR1002', 'peer': 'Urban Core', 'sid': generate_sid()},
            {'name': 'Chase Bank Cincinnati Main', 'id': 'BR1003', 'peer': 'Urban Core', 'sid': generate_sid()},
            {'name': 'Chase Bank Toledo Central', 'id': 'BR1004', 'peer': 'Suburban', 'sid': generate_sid()},
            {'name': 'Chase Bank Dayton Market', 'id': 'BR1005', 'peer': 'Suburban', 'sid': generate_sid()}
        ],
        'Florida': [
            {'name': 'Chase Bank Miami Downtown', 'id': 'BR2001', 'peer': 'Urban Core', 'sid': generate_sid()},
            {'name': 'Chase Bank Orlando Central', 'id': 'BR2002', 'peer': 'Urban Core', 'sid': generate_sid()},
            {'name': 'Chase Bank Tampa Main', 'id': 'BR2003', 'peer': 'Urban Core', 'sid': generate_sid()},
            {'name': 'Chase Bank Jacksonville Plaza', 'id': 'BR2004', 'peer': 'Suburban', 'sid': generate_sid()},
            {'name': 'Chase Bank Tallahassee Center', 'id': 'BR2005', 'peer': 'Suburban', 'sid': generate_sid()}
        ]
    }

    # Category mappings
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

    # Generate date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Generate base scores for each branch that persist across time
    branch_base_scores = {}
    for state, branches in chase_branches.items():
        for branch in branches:
            branch_base_scores[branch['id']] = np.random.normal(75, 5)
    
    data = []
    for date in date_range:
        month = date.strftime('%B')
        year = date.year
        scorecard_period = f"{month} {year}"
        
        for state, branches in chase_branches.items():
            for branch in branches:
                # Use persistent base score for this branch
                base_weighted_score = branch_base_scores[branch['id']]
                performance_tier = determine_performance_tier(base_weighted_score)
                
                for category, subcategories in category_subcategory_mapping.items():
                    category_score = max(0, min(100, base_weighted_score + np.random.normal(0, 2)))
                    
                    for subcategory in subcategories:
                        row = {
                            'Month': month,
                            'Year': year,
                            'Scorecard_Period': scorecard_period,
                            'Division': 'Midwest' if state == 'Ohio' else 'South',
                            'Region': state,
                            'Market': branch['peer'],
                            'Branch_ID': branch['id'],
                            'Branch_Name': branch['name'],
                            'Peer_Group': branch['peer'],
                            'Branch_Manager_SID': branch['sid'],
                            'Overall_Weighted_Score': base_weighted_score,
                            'Performance_Tier': performance_tier,
                            'Category': category,
                            'Subcategory': subcategory,
                            'Value': max(0, min(100, category_score + np.random.normal(0, 1))),
                            'Weight': 15.0,
                            'Weighted_Score': 0,
                            'Peer_Group_Member_Count': np.random.randint(50, 150)
                        }
                        data.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Calculate Weighted Score
    df['Weighted_Score'] = (df['Value'] * df['Weight'] / 100).round(2)
    
    # Print Branch SIDs for verification
    print("\nBranch Manager SIDs:")
    for state, branches in chase_branches.items():
        for branch in branches:
            print(f"{branch['id']}\t{branch['name']}\t{branch['peer']}\t{branch['sid']}")
    
    # Save to Excel
    df.to_excel('scorecard_data_long.xlsx', index=False)
    print(f"\nGenerated {len(df)} records for {len(chase_branches['Ohio'] + chase_branches['Florida'])} branches")
    return df

if __name__ == "__main__":
    df = generate_chase_scorecard_data()
    
    # Print some verification statistics
    print("\nPerformance Tier Distribution:")
    print(df.groupby('Performance_Tier').size())
    
    print("\nSample of generated data:")
    print(df[['Branch_Name', 'Performance_Tier', 'Overall_Weighted_Score']].head())
    
    print("\nData saved to 'scorecard_data_long.xlsx'")