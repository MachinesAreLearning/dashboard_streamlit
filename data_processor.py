# data_processor.py

import pandas as pd
import numpy as np
from datetime import datetime

def load_and_filter_data(division=None, region=None, market=None,branch=None):
    """Load and filter data based on user selections"""
    try:
        # Load the data
        df = pd.read_excel('scorecard_data_long.xlsx')
        
        # Apply filters
        if division and division != "All":
            df = df[df['Division'] == division]
        if region and region != "All":
            df = df[df['Region'] == region]
        if market and market != "All Markets":
            df = df[df['Market'] == market]
        if branch and branch != "All":
            df = df[df['Branch'] == branch]
        return df
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def calculate_main_metrics(df):
    """Calculate main metrics for the dashboard header"""
    if df.empty:
        return {
            'overall_score': 0,
            'overall_rank': 0,
            'pl_distribution': "0% / 0%"
        }
    
    # Calculate metrics
    overall_score = df['Overall_Weighted_Score'].mean()
    
    # Calculate rank - use branch count as a proxy
    overall_rank = len(df['Branch_ID'].unique())
    
    # Calculate PL distribution
    total_branches = len(df['Branch_ID'].unique())
    pl_groups = df.groupby('Branch_ID')['Performance_Tier'].first()
    pl_1_2 = sum(pl_groups.isin(['PL1', 'PL2'])) / total_branches * 100
    pl_5_6 = sum(pl_groups.isin(['PL5', 'PL6'])) / total_branches * 100
    
    return {
        'overall_score': overall_score,
        'overall_rank': overall_rank,
        'pl_distribution': f"{pl_1_2:.1f}% / {pl_5_6:.1f}%"
    }

def calculate_category_metrics(df):
    """Calculate metrics for each category"""
    if df.empty:
        return {}
    
    # Get the latest period
    latest_period = df['Scorecard_Period'].max()
    prev_period = sorted(df['Scorecard_Period'].unique())[-2] if len(df['Scorecard_Period'].unique()) > 1 else latest_period
    
    metrics = {}
    categories = [
        'Growth & One Chase',
        'Customer Experience',
        'Financial Health & Innovation',
        'Culture & Employee',
        'Controls'
    ]
    
    for category in categories:
        category_data = df[df['Category'] == category]
        
        if category_data.empty:
            continue
            
        current_value = category_data[category_data['Scorecard_Period'] == latest_period]['Value'].mean()
        prev_value = category_data[category_data['Scorecard_Period'] == prev_period]['Value'].mean()
        
        vs_last = current_value - prev_value if not pd.isna(prev_value) else 0
        
        metrics[category] = {
            "value": current_value,
            "color": get_category_color(category),
            "vs_last": f"{vs_last:+.1f}%",
            "peer": "+1.0%",  # These could be calculated from peer data
            "national": "+2.0%"  # These could be calculated from national data
        }
    
    return metrics

def get_subcategory_metrics(df, category):
    """Get detailed metrics for each subcategory"""
    if df.empty:
        return []
        
    category_data = df[df['Category'] == category]
    
    if category_data.empty:
        return []
    
    # Get the latest period
    latest_period = category_data['Scorecard_Period'].max()
    category_data = category_data[category_data['Scorecard_Period'] == latest_period]
    
    metrics = []
    for subcategory in category_data['Subcategory'].unique():
        subcat_data = category_data[category_data['Subcategory'] == subcategory]
        value = subcat_data['Value'].mean()
        
        metric = {
            'Metric': subcategory,
            'YTD Sep 24': f"{value:.1f}%",
            'Metric Score': f"{value:.1f}%",
            'Weight': "15.0%",
            'Weighted Score': f"{value * 0.15:.2f}%"
        }
        metrics.append(metric)
    
    return metrics

def get_category_color(category):
    """Get color code for each category"""
    colors = {
        "Growth & One Chase": "#0052CC",
        "Customer Experience": "#00A3BF",
        "Financial Health & Innovation": "#36B37E",
        "Culture & Employee": "#FF8B00",
        "Controls": "#998DD9"
    }
    return colors.get(category, "#666666")