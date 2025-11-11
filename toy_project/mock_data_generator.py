"""
Mock Data Generator for Audience Miner 2.0 Toy Project

Generates realistic synthetic campaign data that mimics digital advertising performance.
"""

import pandas as pd
import numpy as np
from typing import Optional
from datetime import datetime, timedelta


def generate_campaign_data(
    campaign_id: str,
    num_sessions: int = 10000,
    start_date: str = '2024-01-01',
    end_date: str = '2024-12-31',
    seed: Optional[int] = 42
) -> pd.DataFrame:
    """
    Generate synthetic campaign data with realistic performance patterns.

    Args:
        campaign_id: Campaign identifier
        num_sessions: Number of sessions to generate
        start_date: Start date for the campaign (YYYY-MM-DD)
        end_date: End date for the campaign (YYYY-MM-DD)
        seed: Random seed for reproducibility

    Returns:
        DataFrame with synthetic campaign data including demographics and performance metrics

    Output DataFrame columns:
        - campaignId: Campaign identifier
        - date: Date of the session
        - timestamp: Full timestamp
        - sessionid: Unique session ID
        - sourceId: Traffic source/publisher ID
        - age_range: '18-24', '25-34', '35-44', '45-54', '55-64', '65+'
        - income_bucket: '<30K', '30-50K', '50-75K', '75-100K', '100-150K', '>150K'
        - education_level: 'High School', 'Some College', 'Bachelor', 'Graduate', 'Professional'
        - net_asset_value: '<25K', '25-50K', '50-100K', '100-250K', '250-500K', '>500K'
        - homeowner_renter: 'Owner', 'Renter', 'Unknown'
        - children_in_home: 'Yes', 'No', 'Unknown'
        - sessions: Always 1 (per row)
        - viewed_sessions: 1 if position > 0, else 0
        - impressions: Random 1-20 per session
        - clicks: Based on CTR (2-6% base rate)
        - primary_conversion: 1 if converted, 0 otherwise
        - conversions: Same as primary_conversion
        - revenue: $10-80 per conversion

    Performance Patterns (realistic multipliers):
        - Higher income → better performance (1.5x multiplier for '>150K')
        - Higher education → better performance (1.3x for 'Graduate')
        - Age 35-54 → best performance (1.25x multiplier)
        - High net assets → better performance (1.4x for '>500K')
        - Homeowners → slightly better (1.15x multiplier)
    """
    # Set random seed for reproducibility
    if seed is not None:
        np.random.seed(seed)

    # Generate timestamps
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = (end - start).days

    timestamps = [start + timedelta(
        days=np.random.randint(0, date_range),
        hours=np.random.randint(0, 24),
        minutes=np.random.randint(0, 60),
        seconds=np.random.randint(0, 60)
    ) for _ in range(num_sessions)]

    # Define attribute distributions
    age_ranges = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    age_weights = [0.15, 0.25, 0.25, 0.20, 0.10, 0.05]

    income_buckets = ['<30K', '30-50K', '50-75K', '75-100K', '100-150K', '>150K']
    income_weights = [0.15, 0.20, 0.25, 0.20, 0.12, 0.08]

    education_levels = ['High School', 'Some College', 'Bachelor', 'Graduate', 'Professional']
    education_weights = [0.25, 0.25, 0.30, 0.15, 0.05]

    net_asset_values = ['<25K', '25-50K', '50-100K', '100-250K', '250-500K', '>500K']
    nav_weights = [0.20, 0.25, 0.25, 0.15, 0.10, 0.05]

    homeowner_renter = ['Owner', 'Renter', 'Unknown']
    homeowner_weights = [0.50, 0.40, 0.10]

    children_options = ['Yes', 'No', 'Unknown']
    children_weights = [0.35, 0.55, 0.10]

    source_ids = [f'source_{i:03d}' for i in range(1, 21)]

    # Generate base data
    data = {
        'campaignId': [campaign_id] * num_sessions,
        'timestamp': timestamps,
        'date': [ts.strftime('%Y-%m-%d') for ts in timestamps],
        'sessionid': [f'session_{campaign_id}_{i:08d}' for i in range(num_sessions)],
        'sourceId': np.random.choice(source_ids, num_sessions),
        'age_range': np.random.choice(age_ranges, num_sessions, p=age_weights),
        'income_bucket': np.random.choice(income_buckets, num_sessions, p=income_weights),
        'education_level': np.random.choice(education_levels, num_sessions, p=education_weights),
        'net_asset_value': np.random.choice(net_asset_values, num_sessions, p=nav_weights),
        'homeowner_renter': np.random.choice(homeowner_renter, num_sessions, p=homeowner_weights),
        'children_in_home': np.random.choice(children_options, num_sessions, p=children_weights),
        'sessions': [1] * num_sessions,
    }

    df = pd.DataFrame(data)

    # Calculate performance multipliers based on demographics
    df['performance_multiplier'] = 1.0

    # Income effect (1.5x for high income)
    income_multipliers = {
        '<30K': 0.85,
        '30-50K': 0.95,
        '50-75K': 1.0,
        '75-100K': 1.15,
        '100-150K': 1.35,
        '>150K': 1.5
    }
    df['performance_multiplier'] *= df['income_bucket'].map(income_multipliers)

    # Education effect (1.3x for graduate)
    education_multipliers = {
        'High School': 0.9,
        'Some College': 0.95,
        'Bachelor': 1.05,
        'Graduate': 1.3,
        'Professional': 1.25
    }
    df['performance_multiplier'] *= df['education_level'].map(education_multipliers)

    # Age effect (1.25x for 35-54)
    age_multipliers = {
        '18-24': 0.85,
        '25-34': 1.0,
        '35-44': 1.25,
        '45-54': 1.25,
        '55-64': 1.05,
        '65+': 0.9
    }
    df['performance_multiplier'] *= df['age_range'].map(age_multipliers)

    # Net asset value effect (1.4x for high assets)
    nav_multipliers = {
        '<25K': 0.9,
        '25-50K': 0.95,
        '50-100K': 1.0,
        '100-250K': 1.2,
        '250-500K': 1.35,
        '>500K': 1.4
    }
    df['performance_multiplier'] *= df['net_asset_value'].map(nav_multipliers)

    # Homeowner effect (1.15x for owners)
    homeowner_multipliers = {
        'Owner': 1.15,
        'Renter': 1.0,
        'Unknown': 0.95
    }
    df['performance_multiplier'] *= df['homeowner_renter'].map(homeowner_multipliers)

    # Generate performance metrics
    # viewed_sessions: most sessions are viewed
    df['viewed_sessions'] = np.random.choice([0, 1], num_sessions, p=[0.05, 0.95])

    # impressions: 1-20 per session
    df['impressions'] = np.random.randint(1, 21, num_sessions)

    # clicks: based on CTR (2-6% base rate, adjusted by performance multiplier)
    base_ctr = np.random.uniform(0.02, 0.06, num_sessions)
    adjusted_ctr = base_ctr * df['performance_multiplier']
    adjusted_ctr = np.clip(adjusted_ctr, 0, 0.15)  # Cap at 15%
    df['clicks'] = np.random.binomial(df['impressions'], adjusted_ctr)

    # conversions: based on eCR (1-4% base rate, adjusted by performance multiplier)
    base_ecr = np.random.uniform(0.01, 0.04, num_sessions)
    adjusted_ecr = base_ecr * df['performance_multiplier']
    adjusted_ecr = np.clip(adjusted_ecr, 0, 0.12)  # Cap at 12%
    df['primary_conversion'] = np.random.binomial(
        df['viewed_sessions'],
        adjusted_ecr
    )
    df['conversions'] = df['primary_conversion']

    # revenue: $10-80 per conversion
    df['revenue'] = df['conversions'] * np.random.uniform(10, 80, num_sessions)
    df['revenue'] = df['revenue'].round(2)

    # Drop the temporary performance_multiplier column
    df = df.drop('performance_multiplier', axis=1)

    # Reorder columns
    column_order = [
        'campaignId', 'date', 'timestamp', 'sessionid', 'sourceId',
        'age_range', 'income_bucket', 'education_level', 'net_asset_value',
        'homeowner_renter', 'children_in_home', 'sessions', 'viewed_sessions',
        'impressions', 'clicks', 'primary_conversion', 'conversions', 'revenue'
    ]

    return df[column_order]


def save_mock_data(df: pd.DataFrame, filename: str) -> None:
    """
    Save mock data to CSV and print summary statistics.

    Args:
        df: DataFrame to save
        filename: Output CSV filename
    """
    # Save to CSV
    df.to_csv(filename, index=False)

    # Print summary statistics
    print(f"\n✓ Saved {len(df):,} sessions to {filename}")
    print(f"\nSummary Statistics:")
    print(f"  Sessions: {len(df):,}")
    print(f"  Date Range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Total Impressions: {df['impressions'].sum():,}")
    print(f"  Total Clicks: {df['clicks'].sum():,}")
    print(f"  Total Conversions: {df['conversions'].sum():,}")
    print(f"  Total Revenue: ${df['revenue'].sum():,.2f}")

    if df['impressions'].sum() > 0:
        overall_ctr = df['clicks'].sum() / df['impressions'].sum()
        print(f"  Overall CTR: {overall_ctr:.2%}")

    if df['viewed_sessions'].sum() > 0:
        overall_ecr = df['conversions'].sum() / df['viewed_sessions'].sum()
        overall_rps = df['revenue'].sum() / df['viewed_sessions'].sum()
        print(f"  Overall eCR: {overall_ecr:.2%}")
        print(f"  Overall RPS: ${overall_rps:.2f}")


if __name__ == "__main__":
    # Test the data generator
    print("Testing Mock Data Generator...")

    # Generate test data
    test_df = generate_campaign_data(
        campaign_id='TEST_CAMPAIGN',
        num_sessions=5000,
        seed=42
    )

    # Save and display
    save_mock_data(test_df, 'test_campaign_data.csv')

    print("\n✓ Mock data generator working correctly!")
