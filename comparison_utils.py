# comparison_utils.py

import pandas as pd
import streamlit as st

def load_data_versions():
    """
    Load both the current and previous versions of the data
    """
    try:
        current_data = pd.read_csv('branch_data.csv')
        previous_data = pd.read_csv('branch_data_previous.csv')
        return current_data, previous_data
    except Exception as e:
        st.error(f"Error loading comparison data: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()

def create_impact_table(current_df, previous_df, table_type, config):
    """
    Create an impact analysis table showing how changes affect the overall score
    """
    metrics = config['metrics']
    impact_data = []
    
    for metric in metrics:
        ytd_col = metric['ytd_col']
        score_col = metric['score_col']
        weight = metric['weight']
        name = metric['name']
        
        # Skip if columns don't exist in either dataframe
        if ytd_col not in current_df.columns or ytd_col not in previous_df.columns:
            continue
        if score_col not in current_df.columns or score_col not in previous_df.columns:
            continue
            
        try:
            current_ytd = current_df[ytd_col].mean()
            previous_ytd = previous_df[ytd_col].mean()
            current_score = current_df[score_col].mean()
            previous_score = previous_df[score_col].mean()
            
            ytd_delta = current_ytd - previous_ytd
            score_delta = current_score - previous_score
            
            # Calculate impact safely
            impact = 0
            try:
                impact = calculate_impact(score_delta, weight)
            except Exception:
                pass
            
            impact_data.append({
                'Metric': name,
                'Previous': previous_ytd,
                'Current': current_ytd,
                'Delta': ytd_delta,
                'Weight': weight,
                'Impact': impact
            })
        except Exception:
            # Skip this metric if there's an error
            continue
    
    # If no valid metrics were found, return an empty DataFrame
    if not impact_data:
        return pd.DataFrame()
    
    # Create DataFrame from the collected data
    impact_df = pd.DataFrame(impact_data)
    
    # Format the numeric columns
    try:
        impact_df['Impact'] = impact_df['Impact'].apply(lambda x: f"{x:+.2f}%" if isinstance(x, (int, float)) else x)
        impact_df['Delta'] = impact_df['Delta'].apply(lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else x)
        impact_df['Previous'] = impact_df['Previous'].apply(lambda x: f"{x:.1f}%" if isinstance(x, (int, float)) else x)
        impact_df['Current'] = impact_df['Current'].apply(lambda x: f"{x:.1f}%" if isinstance(x, (int, float)) else x)
        impact_df['Weight'] = impact_df['Weight'].apply(lambda x: f"{x:.1f}%" if isinstance(x, (int, float)) else x)
    except Exception:
        # If formatting fails, just continue with unformatted values
        pass
    
    # Calculate total impact in a safer way
    total_impact = 0
    for _, row in impact_df.iterrows():
        try:
            if isinstance(row['Impact'], str):
                # Extract numeric value from Impact column if it's a string
                impact_value = float(row['Impact'].replace('%', '').replace('+', ''))
            else:
                # Use the value directly if it's already numeric
                impact_value = row['Impact']
                
            total_impact += impact_value
        except (ValueError, TypeError):
            # Skip this row if conversion fails
            pass
    
    # Create total row
    total_row = {
        'Metric': 'Total Impact',
        'Previous': '',
        'Current': '',
        'Delta': '',
        'Weight': f"{config['total_weight']:.1f}%" if isinstance(config['total_weight'], (int, float)) else config['total_weight'],
        'Impact': f"{total_impact:+.2f}%"
    }
    
    # Add total row to DataFrame
    impact_df = pd.concat([impact_df, pd.DataFrame([total_row])], ignore_index=True)
    
    return impact_df

def create_comparison_indicator(current_value, previous_value, format_as_percentage=True):
    """
    Create a comparison indicator showing the delta between current and previous values
    """
    if pd.isna(current_value) or pd.isna(previous_value):
        return ""
    
    delta = current_value - previous_value
    if format_as_percentage:
        delta_formatted = f"{delta:+.1f}%" 
    else:
        delta_formatted = f"{delta:+.2f}"
    
    is_positive = delta > 0
    color_class = "positive-value" if is_positive else "negative-value"
    arrow_class = "arrow-up" if is_positive else "arrow-down"
    
    return f'<span class="{color_class} {arrow_class}">{delta_formatted}</span>'

def format_with_delta(current_value, previous_value, format_as_percentage=True):
    """
    Format a value with its delta indicator (e.g., 1.7% → 1.9%, +0.2%)
    """
    if pd.isna(current_value) or pd.isna(previous_value):
        return f"{current_value:.1f}%" if format_as_percentage else f"{current_value:.2f}"
    
    delta = current_value - previous_value
    
    if format_as_percentage:
        current_formatted = f"{current_value:.1f}%"
        previous_formatted = f"{previous_value:.1f}%"
        delta_formatted = f"{delta:+.1f}%" 
    else:
        current_formatted = f"{current_value:.2f}"
        previous_formatted = f"{previous_value:.2f}"
        delta_formatted = f"{delta:+.2f}"
    
    is_positive = delta > 0
    color_class = "positive-value" if is_positive else "negative-value"
    
    return f'{current_formatted} <span class="{color_class}">({previous_formatted} → {delta_formatted})</span>'

def calculate_impact(delta, weight):
    """
    Calculate how a metric's change impacts the overall weighted score
    Weight is given as a percentage (e.g., "15%")
    """
    # Convert string percentage to float if needed
    if isinstance(weight, str):
        weight = float(weight.replace('%', ''))
        
    # Convert string delta to float if needed
    if isinstance(delta, str):
        delta = float(delta.replace('%', '').replace('+', ''))
        
    return (delta * weight) / 100

# Fixed this section - removed the duplicated function and fixed the syntax error
def style_impact_table(df):
    """
    Style the impact analysis table
    """
    def highlight_impact(val):
        if not isinstance(val, str) or not val.endswith('%'):
            return ''
        
        try:
            value = float(val.replace('%', '').replace('+', ''))
            if value > 0:
                return 'color: #40c057; font-weight: 600;'
            elif value < 0:
                return 'color: #fa5252; font-weight: 600;'
            else:
                return ''
        except:
            return ''
    
    def style_rows(row):
        if row.name == len(df) - 1:  # Last row (Total)
            return ['font-weight: 700; background-color: #f0f0f0;'] * len(row)
        return [''] * len(row)
    
    return (df.style
            .apply(style_rows, axis=1)
            .applymap(highlight_impact, subset=['Delta', 'Impact'])
            .set_properties(**{
                'text-align': 'right',
                'padding': '8px 12px',
                'border': '1px solid #e0e0e0'
            })
            .set_properties(subset=['Metric'], **{
                'text-align': 'left',
                'font-weight': '500',
                'color': '#0052CC'
            })
            .set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#f8f9fa'),
                    ('color', '#333'),
                    ('font-weight', '600'),
                    ('text-align', 'center'),
                    ('padding', '10px'),
                    ('border', '1px solid #ddd')
                ]},
                {'selector': 'caption', 'props': [
                    ('caption-side', 'top'),
                    ('font-size', '16px'),
                    ('font-weight', '600'),
                    ('color', '#0052CC'),
                    ('text-align', 'left'),
                    ('padding', '10px 0')
                ]}
            ])
            .set_caption(f"Impact Analysis"))