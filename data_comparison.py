import pandas as pd
import numpy as np
import streamlit as st

def load_comparison_data():
    """
    Load both current and previous versions of the scorecard data
    """
    try:
        current_data = pd.read_csv('branch_data.csv')
        previous_data = pd.read_csv('branch_data_previous.csv')
        return current_data, previous_data
    except Exception as e:
        st.error(f"Error loading comparison data: {str(e)}")
        # If previous version doesn't exist, create a mock one from current with slightly different values
        # This is just for demonstration purposes
        if 'branch_data_previous.csv' in str(e):
            st.warning("Previous version data not found. Using simulated data for demonstration.")
            current_data = pd.read_csv('branch_data.csv')
            previous_data = current_data.copy()
            
            # Modify some values to simulate changes
            for col in previous_data.columns:
                if previous_data[col].dtype in [np.float64, np.int64]:
                    # Add small random variations to numeric columns
                    previous_data[col] = previous_data[col] * np.random.uniform(0.9, 1.1, len(previous_data))
            
            return current_data, previous_data
        return pd.DataFrame(), pd.DataFrame()

def filter_comparison_data(current_df, previous_df, division, region, market, branch):
    """
    Apply filters to both current and previous dataframes
    """
    filtered_current = current_df.copy()
    filtered_previous = previous_df.copy()
    
    # Apply filters to both datasets
    if division != 'All Divisions':
        filtered_current = filtered_current[filtered_current['Division'] == division]
        if 'Division' in filtered_previous.columns:
            filtered_previous = filtered_previous[filtered_previous['Division'] == division]
    
    if region != 'All Regions':
        filtered_current = filtered_current[filtered_current['Region'] == region]
        if 'Region' in filtered_previous.columns:
            filtered_previous = filtered_previous[filtered_previous['Region'] == region]
    
    if market != 'All Markets':
        filtered_current = filtered_current[filtered_current['Market'] == market]
        if 'Market' in filtered_previous.columns:
            filtered_previous = filtered_previous[filtered_previous['Market'] == market]
    
    if branch != 'All Branches':
        filtered_current = filtered_current[filtered_current['Branch'] == branch]
        if 'Branch' in filtered_previous.columns:
            filtered_previous = filtered_previous[filtered_previous['Branch'] == branch]
    
    return filtered_current, filtered_previous

def generate_impact_summary(impact_tables):
    """
    Generate a summary of the most significant impacts across all tables
    """
    all_impacts = pd.DataFrame()
    
    # Combine all impact tables
    for category, impact_df in impact_tables.items():
        if not isinstance(impact_df, pd.DataFrame) or impact_df.empty:
            continue
            
        # Make a copy to avoid modifying original
        df_copy = impact_df.copy()
        
        # Add category column
        df_copy['Category'] = category
        
        # Add to combined dataframe
        all_impacts = pd.concat([all_impacts, df_copy])
    
    # Find top impacts
    if not all_impacts.empty and 'Impact' in all_impacts.columns:
        # Convert Impact to numeric values for sorting
        try:
            all_impacts['Impact_Value'] = all_impacts['Impact'].str.replace('%', '').str.replace('+', '').astype(float)
        except Exception:
            # If conversion fails, return empty dataframes
            return pd.DataFrame(), pd.DataFrame()
            
        # Filter out rows that aren't metrics (like 'Total Impact')
        metrics_df = all_impacts[all_impacts['Metric'] != 'Total Impact']
        
        if not metrics_df.empty:
            # Get top positive impacts
            top_positive = metrics_df[metrics_df['Impact_Value'] > 0].sort_values('Impact_Value', ascending=False).head(3)
            
            # Get top negative impacts
            top_negative = metrics_df[metrics_df['Impact_Value'] < 0].sort_values('Impact_Value', ascending=True).head(3)
            
            return top_positive, top_negative
    
    # Return empty dataframes if no impacts found
    return pd.DataFrame(), pd.DataFrame()

def calculate_change(current_value, previous_value, as_percentage=True):
    """
    Calculate and format the change between current and previous values
    """
    if pd.isna(current_value) or pd.isna(previous_value):
        return ""
    
    delta = current_value - previous_value
    
    if as_percentage:
        return f"{delta:+.1f}%"
    return f"{delta:+.2f}"

def calculate_impact(delta, weight_percentage):
    """
    Calculate how a change in a metric impacts the overall score
    Weight is given as a percentage (e.g., 15%)
    """
    weight = weight_percentage / 100
    return delta * weight

def find_top_impacts(impact_df, n=3):
    """
    Find the top n positive and negative impacts
    """
    # Convert impact column to numeric
    impact_df['Impact_Value'] = impact_df['Impact'].str.replace('%', '').str.replace('+', '').astype(float)
    
    # Sort by impact and get top positive and negative
    positive_impacts = impact_df[impact_df['Impact_Value'] > 0].sort_values('Impact_Value', ascending=False).head(n)
    negative_impacts = impact_df[impact_df['Impact_Value'] < 0].sort_values('Impact_Value', ascending=True).head(n)
    
    return positive_impacts, negative_impacts

def generate_impact_summary(impact_tables):
    """
    Generate a summary of the most significant impacts across all tables
    """
    all_impacts = pd.DataFrame()
    
    # Combine all impact tables
    for category, impact_df in impact_tables.items():
        if not impact_df.empty:
            impact_df['Category'] = category
            all_impacts = pd.concat([all_impacts, impact_df])
    
    # Find top impacts
    if not all_impacts.empty:
        all_impacts['Impact_Value'] = all_impacts['Impact'].str.replace('%', '').str.replace('+', '').astype(float)
        top_positive = all_impacts[all_impacts['Impact_Value'] > 0].sort_values('Impact_Value', ascending=False).head(3)
        top_negative = all_impacts[all_impacts['Impact_Value'] < 0].sort_values('Impact_Value', ascending=True).head(3)
        
        return top_positive, top_negative
    
    return pd.DataFrame(), pd.DataFrame()

def highlight_changes(df, threshold=0.5):
    """
    Add a CSS class to highlight significant changes
    """
    # Convert change column to numeric for comparison
    if 'Change' in df.columns:
        df['Change_Value'] = df['Change'].str.replace('%', '').str.replace('+', '').astype(float)
        df['Highlight'] = df['Change_Value'].abs() >= threshold
        return df
    return df

def create_comparison_view(metric, current_df, previous_df, config):
    """
    Create a detailed comparison view for a specific metric category
    """
    metrics = config['metrics']
    
    comparison_data = []
    for m in metrics:
        ytd_col = m['ytd_col']
        score_col = m['score_col']
        weight = m['weight']
        name = m['name']
        
        # Skip if columns don't exist
        if ytd_col not in current_df.columns or score_col not in current_df.columns:
            continue
        
        current_ytd = current_df[ytd_col].mean()
        current_score = current_df[score_col].mean()
        
        if ytd_col in previous_df.columns and score_col in previous_df.columns:
            previous_ytd = previous_df[ytd_col].mean()
            previous_score = previous_df[score_col].mean()
            
            ytd_delta = current_ytd - previous_ytd
            score_delta = current_score - previous_score
            impact = calculate_impact(score_delta, weight)
            
            comparison_data.append({
                'Metric': name,
                'Previous YTD': f"{previous_ytd:.1f}%",
                'Current YTD': f"{current_ytd:.1f}%",
                'YTD Change': f"{ytd_delta:+.1f}%",
                'Previous Score': f"{previous_score:.1f}%",
                'Current Score': f"{current_score:.1f}%",
                'Score Change': f"{score_delta:+.1f}%",
                'Weight': f"{weight:.1f}%",
                'Impact': f"{impact:+.2f}%"
            })
    
    return pd.DataFrame(comparison_data)

def generate_explanation(metric_name, previous, current, weight):
    """
    Generate a natural language explanation of a metric's change and impact
    """
    delta = current - previous
    impact = calculate_impact(delta, weight)
    
    if delta > 0:
        change_description = f"increased by {delta:.1f}%"
    elif delta < 0:
        change_description = f"decreased by {abs(delta):.1f}%"
    else:
        change_description = "remained unchanged"
    
    explanation = f"{metric_name} {change_description} (from {previous:.1f}% to {current:.1f}%)."
    
    if impact != 0:
        if impact > 0:
            impact_description = f"This improvement contributed +{impact:.2f}% to the overall score."
        else:
            impact_description = f"This decline reduced the overall score by {abs(impact):.2f}%."
        
        explanation += f" {impact_description}"
    
    return explanation