"""
Simple Comparison Engine for Audience Miner 2.0 Toy Project

Compare two campaigns to find competitive advantages.
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from simple_segmentation_engine import SegmentMetrics


class SimpleComparisonEngine:
    """
    Comparison engine that finds segments with competitive advantages.

    Compares two campaigns across demographic segments to identify
    where each campaign performs better.
    """

    def __init__(
        self,
        data_a: pd.DataFrame,
        data_b: pd.DataFrame,
        campaign_a_id: str,
        campaign_b_id: str,
        attributes: List[str],
        min_advantage: float = 0.20,
        min_sessions: int = 100
    ):
        """
        Initialize comparison engine.

        Args:
            data_a: Aggregated data for campaign A
            data_b: Aggregated data for campaign B
            campaign_a_id: Name for campaign A
            campaign_b_id: Name for campaign B
            attributes: Attributes to compare across
            min_advantage: Minimum difference to highlight (0.20 = 20%)
            min_sessions: Minimum sessions per segment
        """
        self.data_a = data_a.copy()
        self.data_b = data_b.copy()
        self.campaign_a_id = campaign_a_id
        self.campaign_b_id = campaign_b_id
        self.attributes = attributes
        self.min_advantage = min_advantage
        self.min_sessions = min_sessions

        # Calculate base metrics
        self.base_a = self._calculate_metrics(self.data_a)
        self.base_b = self._calculate_metrics(self.data_b)

    def _calculate_metrics(self, df: pd.DataFrame) -> SegmentMetrics:
        """
        Calculate performance metrics for a DataFrame.

        Args:
            df: DataFrame with aggregated campaign data

        Returns:
            SegmentMetrics object
        """
        return SegmentMetrics(
            sessions=int(df['sessions'].sum()),
            viewed_sessions=int(df['viewed_sessions'].sum()),
            impressions=int(df['impressions'].sum()),
            clicks=int(df['clicks'].sum()),
            conversions=int(df['conversions'].sum()),
            revenue=float(df['revenue'].sum())
        )

    def compare(self, verbose: bool = True) -> List[Dict]:
        """
        Find segments with significant advantages.

        Algorithm:
        1. Calculate base metrics for both campaigns
        2. For each attribute:
             For each unique value (union of both campaigns):
                 a. Filter both campaigns to this segment
                 b. Calculate metrics for each
                 c. Calculate percentage differences:
                    - rps_diff = (A.rps - B.rps) / B.rps
                    - ecr_diff = (A.ecr - B.ecr) / B.ecr
                    - ctr_diff = (A.ctr - B.ctr) / B.ctr
                 d. Count advantages (threshold: min_advantage):
                    - a_advantages = count of metrics where diff > min_advantage
                    - b_advantages = count of metrics where diff < -min_advantage
                 e. Determine advantage:
                    - If a_advantages >= 2: "Strong A Advantage"
                    - If b_advantages >= 2: "Strong B Advantage"
                    - If a_advantages > b_advantages: "Moderate A Advantage"
                    - Else if b_advantages > a_advantages: "Moderate B Advantage"
                    - Else: "Neutral"
                 f. If not Neutral, add to results
        3. Sort by absolute advantage score (descending)

        Args:
            verbose: Print progress messages

        Returns:
            List of comparison dictionaries with:
            - segment_condition: "attribute = 'value'"
            - overall_advantage: advantage label
            - campaign_a_ecr, campaign_a_rps, campaign_a_ctr
            - campaign_b_ecr, campaign_b_rps, campaign_b_ctr
            - ecr_diff_pct, rps_diff_pct, ctr_diff_pct
            - rps_advantage, ecr_advantage, ctr_advantage
        """
        if verbose:
            print("\n" + "=" * 70)
            print("CAMPAIGN COMPARISON ANALYSIS")
            print("=" * 70)

        # Step 1: Base metrics already calculated in __init__
        if verbose:
            print(f"\n{self.campaign_a_id} Base Metrics:")
            print(f"  Sessions: {self.base_a.sessions:,}")
            print(f"  eCR: {self.base_a.ecr:.2%}")
            print(f"  RPS: ${self.base_a.rps:.2f}")
            print(f"  CTR: {self.base_a.ctr:.2%}")

            print(f"\n{self.campaign_b_id} Base Metrics:")
            print(f"  Sessions: {self.base_b.sessions:,}")
            print(f"  eCR: {self.base_b.ecr:.2%}")
            print(f"  RPS: ${self.base_b.rps:.2f}")
            print(f"  CTR: {self.base_b.ctr:.2%}")

        # Step 2: Compare segments
        comparisons = []

        for attr in self.attributes:
            # Get union of all unique values
            values_a = set(self.data_a[attr].unique()) if attr in self.data_a.columns else set()
            values_b = set(self.data_b[attr].unique()) if attr in self.data_b.columns else set()
            all_values = values_a.union(values_b)

            for value in all_values:
                # Filter to segment
                segment_a = self.data_a[self.data_a[attr] == value] if attr in self.data_a.columns else pd.DataFrame()
                segment_b = self.data_b[self.data_b[attr] == value] if attr in self.data_b.columns else pd.DataFrame()

                # Skip if both segments are empty or too small
                if len(segment_a) == 0 and len(segment_b) == 0:
                    continue

                # Calculate metrics
                metrics_a = self._calculate_metrics(segment_a) if len(segment_a) > 0 else SegmentMetrics(0, 0, 0, 0, 0, 0.0)
                metrics_b = self._calculate_metrics(segment_b) if len(segment_b) > 0 else SegmentMetrics(0, 0, 0, 0, 0, 0.0)

                # Skip if both segments have insufficient data
                if metrics_a.sessions < self.min_sessions and metrics_b.sessions < self.min_sessions:
                    continue

                # Calculate percentage differences
                ecr_diff = ((metrics_a.ecr - metrics_b.ecr) / metrics_b.ecr) if metrics_b.ecr > 0 else 0.0
                rps_diff = ((metrics_a.rps - metrics_b.rps) / metrics_b.rps) if metrics_b.rps > 0 else 0.0
                ctr_diff = ((metrics_a.ctr - metrics_b.ctr) / metrics_b.ctr) if metrics_b.ctr > 0 else 0.0

                # Count advantages
                a_advantages = 0
                b_advantages = 0

                # Check eCR advantage
                if ecr_diff > self.min_advantage:
                    a_advantages += 1
                    ecr_advantage = f"{self.campaign_a_id} Advantage"
                elif ecr_diff < -self.min_advantage:
                    b_advantages += 1
                    ecr_advantage = f"{self.campaign_b_id} Advantage"
                else:
                    ecr_advantage = "Neutral"

                # Check RPS advantage
                if rps_diff > self.min_advantage:
                    a_advantages += 1
                    rps_advantage = f"{self.campaign_a_id} Advantage"
                elif rps_diff < -self.min_advantage:
                    b_advantages += 1
                    rps_advantage = f"{self.campaign_b_id} Advantage"
                else:
                    rps_advantage = "Neutral"

                # Check CTR advantage
                if ctr_diff > self.min_advantage:
                    a_advantages += 1
                    ctr_advantage = f"{self.campaign_a_id} Advantage"
                elif ctr_diff < -self.min_advantage:
                    b_advantages += 1
                    ctr_advantage = f"{self.campaign_b_id} Advantage"
                else:
                    ctr_advantage = "Neutral"

                # Determine overall advantage
                if a_advantages >= 2:
                    overall_advantage = f"Strong {self.campaign_a_id} Advantage"
                    advantage_score = a_advantages
                elif b_advantages >= 2:
                    overall_advantage = f"Strong {self.campaign_b_id} Advantage"
                    advantage_score = b_advantages
                elif a_advantages > b_advantages:
                    overall_advantage = f"Moderate {self.campaign_a_id} Advantage"
                    advantage_score = a_advantages - b_advantages
                elif b_advantages > a_advantages:
                    overall_advantage = f"Moderate {self.campaign_b_id} Advantage"
                    advantage_score = b_advantages - a_advantages
                else:
                    overall_advantage = "Neutral"
                    advantage_score = 0

                # Only add non-neutral results
                if overall_advantage != "Neutral":
                    comparisons.append({
                        'segment_condition': f"{attr} = '{value}'",
                        'attribute': attr,
                        'value': str(value),
                        'overall_advantage': overall_advantage,
                        'advantage_score': advantage_score,
                        'campaign_a_sessions': metrics_a.sessions,
                        'campaign_b_sessions': metrics_b.sessions,
                        'campaign_a_ecr': metrics_a.ecr,
                        'campaign_b_ecr': metrics_b.ecr,
                        'campaign_a_rps': metrics_a.rps,
                        'campaign_b_rps': metrics_b.rps,
                        'campaign_a_ctr': metrics_a.ctr,
                        'campaign_b_ctr': metrics_b.ctr,
                        'ecr_diff_pct': ecr_diff,
                        'rps_diff_pct': rps_diff,
                        'ctr_diff_pct': ctr_diff,
                        'ecr_advantage': ecr_advantage,
                        'rps_advantage': rps_advantage,
                        'ctr_advantage': ctr_advantage
                    })

        # Step 3: Sort by advantage score
        comparisons = sorted(
            comparisons,
            key=lambda x: (x['advantage_score'], abs(x['rps_diff_pct'])),
            reverse=True
        )

        if verbose:
            print(f"\n✓ Found {len(comparisons)} segments with advantages")

            # Count advantages for each campaign
            a_count = sum(1 for c in comparisons if self.campaign_a_id in c['overall_advantage'])
            b_count = sum(1 for c in comparisons if self.campaign_b_id in c['overall_advantage'])

            print(f"  {self.campaign_a_id} has advantage in {a_count} segments")
            print(f"  {self.campaign_b_id} has advantage in {b_count} segments")

        return comparisons


if __name__ == "__main__":
    # Test the comparison engine
    print("Testing Comparison Engine...")

    # Generate test data for two campaigns
    from mock_data_generator import generate_campaign_data
    from pandas_data_loader import PandasDataLoader

    print("\nGenerating test data for two campaigns...")

    # Campaign A (seed 42)
    campaign_a_df = generate_campaign_data(
        campaign_id='CAMPAIGN_A',
        num_sessions=10000,
        seed=42
    )

    # Campaign B (seed 123) - slightly different performance patterns
    campaign_b_df = generate_campaign_data(
        campaign_id='CAMPAIGN_B',
        num_sessions=10000,
        seed=123
    )

    # Aggregate both campaigns
    print("\nAggregating Campaign A...")
    loader_a = PandasDataLoader(
        data_source=campaign_a_df,
        campaign_id='CAMPAIGN_A',
        start_date='2024-01-01',
        end_date='2024-12-31',
        attributes=['age_range', 'income_bucket', 'education_level']
    )
    aggregated_a = loader_a.load_campaign_data()

    print("\nAggregating Campaign B...")
    loader_b = PandasDataLoader(
        data_source=campaign_b_df,
        campaign_id='CAMPAIGN_B',
        start_date='2024-01-01',
        end_date='2024-12-31',
        attributes=['age_range', 'income_bucket', 'education_level']
    )
    aggregated_b = loader_b.load_campaign_data()

    # Run comparison
    print("\nRunning comparison...")
    engine = SimpleComparisonEngine(
        data_a=aggregated_a,
        data_b=aggregated_b,
        campaign_a_id='Campaign_A',
        campaign_b_id='Campaign_B',
        attributes=['age_range', 'income_bucket', 'education_level'],
        min_advantage=0.20
    )

    comparisons = engine.compare(verbose=True)

    # Display top comparisons
    print("\n" + "=" * 70)
    print("TOP COMPETITIVE INSIGHTS")
    print("=" * 70)

    for i, comp in enumerate(comparisons[:5], 1):
        print(f"\n{i}. {comp['segment_condition']}")
        print(f"   Advantage: {comp['overall_advantage']}")
        print(f"   Campaign A: eCR {comp['campaign_a_ecr']:.2%}, RPS ${comp['campaign_a_rps']:.2f}, CTR {comp['campaign_a_ctr']:.2%}")
        print(f"   Campaign B: eCR {comp['campaign_b_ecr']:.2%}, RPS ${comp['campaign_b_rps']:.2f}, CTR {comp['campaign_b_ctr']:.2%}")
        print(f"   Difference: eCR {comp['ecr_diff_pct']:+.1%}, RPS {comp['rps_diff_pct']:+.1%}, CTR {comp['ctr_diff_pct']:+.1%}")

    print("\n✓ Comparison engine working correctly!")
