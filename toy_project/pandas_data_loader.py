"""
Pandas Data Loader for Audience Miner 2.0 Toy Project

Loads and aggregates campaign data using Pandas (replaces Spark in production).
"""

import pandas as pd
from typing import Union, List, Optional, Tuple
from datetime import datetime


class PandasDataLoader:
    """
    Data loader that uses Pandas for loading and aggregating campaign data.

    This replaces the Spark-based data loader used in production.
    """

    def __init__(
        self,
        data_source: Union[str, pd.DataFrame],
        campaign_id: str,
        start_date: str,
        end_date: str,
        attributes: List[str],
        source_id: Optional[str] = None,
        excluded_sources: Optional[List[str]] = None
    ):
        """
        Initialize data loader.

        Args:
            data_source: CSV filename or DataFrame
            campaign_id: Campaign to filter
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            attributes: List of attributes to group by
            source_id: Optional specific source to analyze
            excluded_sources: List of sources to exclude
        """
        self.data_source = data_source
        self.campaign_id = campaign_id
        self.start_date = start_date
        self.end_date = end_date
        self.attributes = attributes
        self.source_id = source_id
        self.excluded_sources = excluded_sources or []

    def load_campaign_data(self) -> pd.DataFrame:
        """
        Load and aggregate campaign data.

        Process:
        1. Load from CSV or use DataFrame
        2. Filter by campaign_id
        3. Filter by date range
        4. Filter by source_id (if specified)
        5. Exclude sources (if specified)
        6. Aggregate by attributes

        Aggregation (GROUP BY attributes):
        - sessions: COUNT(DISTINCT sessionid)
        - viewed_sessions: SUM(viewed_sessions)
        - impressions: SUM(impressions)
        - clicks: SUM(clicks)
        - conversions: SUM(primary_conversion)
        - revenue: SUM(revenue)

        Returns:
            Aggregated DataFrame
        """
        # Step 1: Load data
        if isinstance(self.data_source, str):
            print(f"Loading data from {self.data_source}...")
            df = pd.read_csv(self.data_source)
        else:
            df = self.data_source.copy()

        initial_rows = len(df)
        print(f"  Initial rows: {initial_rows:,}")

        # Step 2: Filter by campaign_id
        if 'campaignId' in df.columns:
            df = df[df['campaignId'] == self.campaign_id]
            print(f"  After campaign filter: {len(df):,} rows")

        # Step 3: Filter by date range
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            start = pd.to_datetime(self.start_date)
            end = pd.to_datetime(self.end_date)
            df = df[(df['date'] >= start) & (df['date'] <= end)]
            print(f"  After date filter: {len(df):,} rows")

        # Step 4: Filter by source_id (if specified)
        if self.source_id and 'sourceId' in df.columns:
            df = df[df['sourceId'] == self.source_id]
            print(f"  After source filter: {len(df):,} rows")

        # Step 5: Exclude sources (if specified)
        if self.excluded_sources and 'sourceId' in df.columns:
            df = df[~df['sourceId'].isin(self.excluded_sources)]
            print(f"  After exclusion filter: {len(df):,} rows")

        if len(df) == 0:
            print("  WARNING: No data after filtering!")
            return pd.DataFrame()

        # Step 6: Aggregate by attributes
        print(f"  Aggregating by: {', '.join(self.attributes)}")

        # Define aggregation operations
        agg_dict = {
            'sessionid': 'nunique',  # COUNT DISTINCT
            'viewed_sessions': 'sum',
            'impressions': 'sum',
            'clicks': 'sum',
            'conversions': 'sum',
            'revenue': 'sum'
        }

        # Handle primary_conversion vs conversions
        if 'primary_conversion' in df.columns and 'conversions' not in agg_dict:
            agg_dict['primary_conversion'] = 'sum'

        # Perform aggregation
        aggregated = df.groupby(self.attributes, as_index=False).agg(agg_dict)

        # Rename columns
        aggregated = aggregated.rename(columns={
            'sessionid': 'sessions',
            'primary_conversion': 'conversions'
        })

        # Ensure conversions column exists
        if 'conversions' not in aggregated.columns and 'primary_conversion' in aggregated.columns:
            aggregated['conversions'] = aggregated['primary_conversion']

        print(f"  ✓ Aggregated to {len(aggregated):,} segments")

        return aggregated

    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
        """
        Preprocess data: normalize, identify types, clean.

        Args:
            df: Aggregated DataFrame

        Returns:
            Tuple of (processed_df, numeric_features, categorical_features)
        """
        processed_df = df.copy()

        # Identify numeric and categorical features
        numeric_features = []
        categorical_features = []

        for col in processed_df.columns:
            if col in ['sessions', 'viewed_sessions', 'impressions', 'clicks', 'conversions', 'revenue']:
                numeric_features.append(col)
            elif col in self.attributes:
                categorical_features.append(col)
                # Ensure categorical columns are strings
                processed_df[col] = processed_df[col].astype(str)

        # Fill any missing values in numeric columns with 0
        for col in numeric_features:
            if col in processed_df.columns:
                processed_df[col] = processed_df[col].fillna(0)

        # Fill any missing values in categorical columns with 'Unknown'
        for col in categorical_features:
            if col in processed_df.columns:
                processed_df[col] = processed_df[col].fillna('Unknown')

        print(f"\nData preprocessing complete:")
        print(f"  Numeric features: {len(numeric_features)}")
        print(f"  Categorical features: {len(categorical_features)}")

        return processed_df, numeric_features, categorical_features


def load_and_aggregate(
    csv_file: str,
    campaign_id: str,
    attributes: List[str],
    start_date: str = '2024-01-01',
    end_date: str = '2024-12-31',
    source_id: Optional[str] = None,
    excluded_sources: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Convenience function to load and aggregate data in one step.

    Args:
        csv_file: Path to CSV file
        campaign_id: Campaign identifier
        attributes: List of attributes to group by
        start_date: Start date filter
        end_date: End date filter
        source_id: Optional source filter
        excluded_sources: Optional list of sources to exclude

    Returns:
        Aggregated DataFrame
    """
    loader = PandasDataLoader(
        data_source=csv_file,
        campaign_id=campaign_id,
        start_date=start_date,
        end_date=end_date,
        attributes=attributes,
        source_id=source_id,
        excluded_sources=excluded_sources
    )

    return loader.load_campaign_data()


if __name__ == "__main__":
    # Test the data loader
    print("Testing Pandas Data Loader...")

    # First generate some test data
    from mock_data_generator import generate_campaign_data, save_mock_data

    print("\nGenerating test data...")
    test_df = generate_campaign_data(
        campaign_id='TEST_CAMPAIGN',
        num_sessions=5000,
        seed=42
    )
    save_mock_data(test_df, 'test_loader_data.csv')

    # Test loading and aggregation
    print("\n" + "=" * 70)
    print("Testing data loading and aggregation...")
    print("=" * 70)

    loader = PandasDataLoader(
        data_source='test_loader_data.csv',
        campaign_id='TEST_CAMPAIGN',
        start_date='2024-01-01',
        end_date='2024-12-31',
        attributes=['age_range', 'income_bucket']
    )

    aggregated_df = loader.load_campaign_data()

    print("\n" + "=" * 70)
    print("Sample aggregated data:")
    print("=" * 70)
    print(aggregated_df.head(10))

    print("\n" + "=" * 70)
    print("Summary of aggregated data:")
    print("=" * 70)
    print(f"Total segments: {len(aggregated_df)}")
    print(f"Total sessions: {aggregated_df['sessions'].sum():,}")
    print(f"Total conversions: {aggregated_df['conversions'].sum():,}")
    print(f"Total revenue: ${aggregated_df['revenue'].sum():,.2f}")

    print("\n✓ Pandas data loader working correctly!")
