# utils.py

def create_metric_box(label, value):
    return f"""
    <div class="metric-container">
        <div class="ytd-label-top">YTD</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value if value != 'N/A' else 'No Data'}</div>
    </div>
    """

def create_metric_box_0(label, value):
    return f"""
    <div class="metric-container">
        <div class="ytd-label-top">YTD</div>
        <div class="metric-label-2">{label}</div>
        <div class="metric-value">{value if value != 'N/A' else 'No Data'}</div>
    </div>
    """

def create_comparison_metric(value):
    is_positive = not str(value).startswith('-')
    color_class = "positive-value" if is_positive else "negative-value"
    arrow_class = "arrow-up" if is_positive else "arrow-down"
    return f'<span class="{color_class} {arrow_class}">{value}</span>'

def calculate_comparison(df, column_name):
    try:
        value = df[column_name].mean()
        return f"{'+' if value > 0 else ''}{value:.1f}%"
    except:
        return "0.0%"

def style_dataframe(df):
    def style_rows(row):
        is_total = row['Metric'] == 'Total'
        style = []
        
        for col in row.index:
            if is_total:
                style.append('''
                    background-color: #f9f9f9; 
                    font-weight: 700;
                    border-top: 2px solid #e6e6e6;
                ''')
            elif row.name % 2 == 0:
                style.append('background-color: white;')
            else:
                style.append('background-color: #f9f9f9;')
        return style
    
    return (df.style
        .apply(style_rows, axis=1)
        .format({
            'YTD Sep 24': lambda x: x if x else '',
            'Metric Score': lambda x: x if x else '',
            'Weight': lambda x: x if x else '',
            'Weighted Score': lambda x: x if x else ''
        })
        .set_properties(**{
            'padding': '8px 16px',
            'border-bottom': '1px solid #e6e6e6',
            'text-align': 'right'
        })
        .set_properties(subset=['Metric'], **{
            'text-align': 'left',
            'font-weight': '500',
            'color': '#0052CC',
            'border-right': '2px solid #f0f0f0'
        })
        .set_table_styles([
            {'selector': 'th', 'props': [
                ('background-color', 'white'),
                ('color', '#666'),
                ('font-weight', '400'),
                ('text-align', 'left'),
                ('padding', '8px 16px'),
                ('border-bottom', '2px solid #e6e6e6')
            ]},
            {'selector': 'th:not(:first-child)', 'props': [
                ('text-align', 'right')
            ]},
            {'selector': 'th:first-child', 'props': [
                ('border-right', '2px solid #f0f0f0'),
                ('color', '#0052CC')
            ]}
        ]))