# config.py

METRICS_CONFIG = {
    "Growth & One Chase (60%)": {
        "max_value": 60.0,
        "color": "#0052CC",
        "score_column": "growth_score",
        "comparison_columns": {
            "vs_last": "gologin",
            "peer": "gocredicard",
            "national": "cobranchosat"
        }
    },
    "Customer Experience (15%)": {
        "max_value": 15.0,
        "color": "#00A3BF",
        "score_column": "customer_exp_score",
        "comparison_columns": {
            "vs_last": "gologin",
            "peer": "gocredicard",
            "national": "cobranchosat"
        }
    },
    "Financial Health & Innovation (15%)": {
        "max_value": 15.0,
        "color": "#36B37E",
        "score_column": "financial_health_score",
        "comparison_columns": {
            "vs_last": "gologin",
            "peer": "gocredicard",
            "national": "cobranchosat"
        }
    },
    "Culture & Employee (5%)": {
        "max_value": 5.0,
        "color": "#FF8B00",
        "score_column": "culture_score",
        "comparison_columns": {
            "vs_last": "gologin",
            "peer": "gocredicard",
            "national": "cobranchosat"
        }
    },
    "Controls (5%)": {
        "max_value": 5.0,
        "color": "#998DD9",
        "score_column": "controls_score",
        "comparison_columns": {
            "vs_last": "gologin",
            "peer": "gocredicard",
            "national": "cobranchosat"
        }
    }
}

TABLE_CONFIGS = {
    'growth': {
        'title': 'Growth & One Chase',
        'metrics': [
            {'name': 'Net Checking Acquisition', 'ytd_col': 'nca_ytd', 'score_col': 'nca_score', 'weight': 7.5},
            {'name': 'Banker Coverage of Calls/Meeting', 'ytd_col': 'banker_ytd', 'score_col': 'banker_score', 'weight': 5.0},
            {'name': 'Discover Needs at NAO', 'ytd_col': 'discover_ytd', 'score_col': 'discover_score', 'weight': 5.0},
            {'name': 'First Time Investors Ratio', 'ytd_col': 'investors_ytd', 'score_col': 'investors_score', 'weight': 10.0},
            {'name': 'Loan Originations', 'ytd_col': 'loan_ytd', 'score_col': 'loan_score', 'weight': 7.5},
            {'name': 'Credit Card Activations Ratio', 'ytd_col': 'cc_ytd', 'score_col': 'cc_score', 'weight': 10.0},
            {'name': 'Total DDA Balance Growth', 'ytd_col': 'dda_ytd', 'score_col': 'dda_score', 'weight': 15.0}
        ],
        'total_weight': 60.0
    },
    'customer': {
        'title': 'Customer Experience',
        'metrics': [
            {'name': 'Branch OSAT', 'ytd_col': 'osat_ytd', 'score_col': 'osat_score', 'weight': 15.0}
        ],
        'total_weight': 15.0
    },
    'financial': {
        'title': 'Financial Health & Innovation',
        'metrics': [
            {'name': 'Digital Adoption', 'ytd_col': 'digital_ytd', 'score_col': 'digital_score', 'weight': 7.5},
            {'name': 'Financial Health Conversations', 'ytd_col': 'health_ytd', 'score_col': 'health_score', 'weight': 7.5}
        ],
        'total_weight': 15.0
    },
    'controls': {
        'title': 'Controls',
        'metrics': [
            {'name': 'Risk Assessment', 'ytd_col': 'risk_ytd', 'score_col': 'risk_score', 'weight': 2.5},
            {'name': 'Compliance Rating', 'ytd_col': 'compliance_ytd', 'score_col': 'compliance_score', 'weight': 2.5}
        ],
        'total_weight': 5.0
    }
}