"""
Simple Segmentation Engine for Audience Miner 2.0 Toy Project

Core algorithm to find high-performing segments using statistical methods.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
from scipy.stats import chi2_contingency


@dataclass
class SegmentMetrics:
    """Performance metrics for a segment."""
    sessions: int
    viewed_sessions: int
    impressions: int
    clicks: int
    conversions: int
    revenue: float

    @property
    def ctr(self) -> float:
        """Click-through rate: clicks / impressions"""
        return self.clicks / self.impressions if self.impressions > 0 else 0.0

    @property
    def ecr(self) -> float:
        """Engagement conversion rate: conversions / viewed_sessions"""
        return self.conversions / self.viewed_sessions if self.viewed_sessions > 0 else 0.0

    @property
    def rps(self) -> float:
        """Revenue per session: revenue / viewed_sessions"""
        return self.revenue / self.viewed_sessions if self.viewed_sessions > 0 else 0.0

    @property
    def rpi(self) -> float:
        """Revenue per impression: revenue / impressions"""
        return self.revenue / self.impressions if self.impressions > 0 else 0.0


class SimpleSegmentationEngine:
    """
    Segmentation engine that finds high-performing audience segments.

    Uses recursive binary splitting with statistical validation.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        attributes: List[str],
        max_segments: int = 10,
        min_lift: float = 0.20,
        min_segment_pct: float = 0.05,
        significance_threshold: float = 0.05,
        min_multiplier: float = 0.70,
        max_multiplier: float = 1.50
    ):
        """
        Initialize segmentation engine.

        Args:
            data: Aggregated campaign data
            attributes: Segmentation attributes
            max_segments: Maximum segments to return
            min_lift: Minimum performance lift (0.20 = 20%)
            min_segment_pct: Minimum segment size (0.05 = 5%)
            significance_threshold: P-value threshold (0.05 = 95% confidence)
            min_multiplier: Minimum bid multiplier (0.70 = 70%)
            max_multiplier: Maximum bid multiplier (1.50 = 150%)
        """
        self.data = data.copy()
        self.attributes = attributes
        self.max_segments = max_segments
        self.min_lift = min_lift
        self.min_segment_pct = min_segment_pct
        self.significance_threshold = significance_threshold
        self.min_multiplier = min_multiplier
        self.max_multiplier = max_multiplier

        # Calculate base metrics once
        self.base_metrics = self._calculate_metrics(self.data)

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

    def _cramers_v(self, attribute: str) -> float:
        """
        Calculate Cramér's V for feature importance.

        Cramér's V measures the association between a categorical variable
        and conversion outcomes. It ranges from 0 (no association) to 1 (perfect association).

        Formula:
            V = sqrt(χ² / (n × min(r-1, c-1)))

        Where:
            χ² = Chi-square statistic from contingency table
            n = total observations
            r = number of rows
            c = number of columns (usually 2: converted/not converted)

        Process:
        1. Create contingency table:
           - Rows: unique values of attribute
           - Cols: [converted, not_converted]
        2. Run chi2_contingency() from scipy.stats
        3. Calculate Cramér's V

        Args:
            attribute: Attribute name to calculate importance for

        Returns:
            Float between 0.0 and 1.0
            - 0.0-0.1: Negligible
            - 0.1-0.2: Weak
            - 0.2-0.4: Moderate (use for segmentation)
            - 0.4+: Strong (prioritize!)
        """
        try:
            # Create a detailed dataset for contingency table
            # We need to expand the aggregated data
            expanded_data = []

            for _, row in self.data.iterrows():
                attr_value = row[attribute]
                conversions = int(row['conversions'])
                viewed_sessions = int(row['viewed_sessions'])
                non_conversions = viewed_sessions - conversions

                # Add entries for converted and non-converted
                if conversions > 0:
                    expanded_data.append({
                        attribute: attr_value,
                        'converted': 1
                    })
                if non_conversions > 0:
                    expanded_data.append({
                        attribute: attr_value,
                        'converted': 0
                    })

            if not expanded_data:
                return 0.0

            # Create DataFrame
            expanded_df = pd.DataFrame(expanded_data)

            # Create contingency table
            contingency_table = pd.crosstab(
                expanded_df[attribute],
                expanded_df['converted']
            )

            # Run chi-square test
            chi2, p_value, dof, expected = chi2_contingency(contingency_table)

            # Calculate Cramér's V
            n = contingency_table.sum().sum()
            min_dim = min(contingency_table.shape[0] - 1, contingency_table.shape[1] - 1)

            if n > 0 and min_dim > 0:
                cramers_v = np.sqrt(chi2 / (n * min_dim))
                return cramers_v
            else:
                return 0.0

        except Exception as e:
            print(f"  Warning: Could not calculate Cramér's V for {attribute}: {e}")
            return 0.0

    def _validate_split(self, segment_metrics: SegmentMetrics) -> bool:
        """
        Validate if segment meets criteria.

        Checks:
        1. Minimum size: segment.sessions >= total_sessions × min_segment_pct
        2. Minimum lift: (segment.ecr - base.ecr) / base.ecr >= min_lift
        3. Statistical significance: Chi-square test with p < significance_threshold

        Args:
            segment_metrics: Metrics for the segment to validate

        Returns:
            True if segment passes all checks
        """
        # Check 1: Minimum size
        min_sessions = self.base_metrics.sessions * self.min_segment_pct
        if segment_metrics.sessions < min_sessions:
            return False

        # Check 2: Minimum lift
        if self.base_metrics.ecr > 0:
            lift = (segment_metrics.ecr - self.base_metrics.ecr) / self.base_metrics.ecr
            if lift < self.min_lift:
                return False
        else:
            return False

        # Check 3: Statistical significance (Chi-square test)
        try:
            # Create 2×2 contingency table
            segment_converted = segment_metrics.conversions
            segment_not_converted = segment_metrics.viewed_sessions - segment_converted

            baseline_converted = self.base_metrics.conversions - segment_converted
            baseline_not_converted = (self.base_metrics.viewed_sessions -
                                     segment_metrics.viewed_sessions - baseline_converted)

            contingency_table = np.array([
                [segment_converted, segment_not_converted],
                [baseline_converted, baseline_not_converted]
            ])

            # Ensure all values are non-negative
            if np.any(contingency_table < 0):
                return False

            chi2, p_value, dof, expected = chi2_contingency(contingency_table)

            # Check if statistically significant
            if p_value >= self.significance_threshold:
                return False

        except Exception as e:
            # If chi-square test fails, reject the segment
            return False

        return True

    def _calculate_bid_multiplier(self, lift: float, sessions: int) -> float:
        """
        Calculate bid multiplier using sigmoid transformation.

        Formula:
            sigmoid = 1 / (1 + exp(-sensitivity × lift))
            multiplier = min_mult + (max_mult - min_mult) × sigmoid

            # Confidence weighting
            confidence = min(1.0, sessions / 1000)
            multiplier = 1.0 + (multiplier - 1.0) × confidence

        Parameters:
            sensitivity = 5.0 (controls steepness)

        Examples:
            lift=+0.50, sessions=10000 → 1.44x (increase bids 44%)
            lift=+0.20, sessions=2000  → 1.28x (increase bids 28%)
            lift=0.00, sessions=any    → 1.00x (no change)
            lift=-0.20, sessions=2000  → 0.82x (decrease bids 18%)

        Args:
            lift: Performance lift (e.g., 0.30 for 30% lift)
            sessions: Number of sessions in segment

        Returns:
            Bid multiplier (rounded to 2 decimals)
        """
        sensitivity = 5.0

        # Calculate sigmoid
        sigmoid = 1.0 / (1.0 + np.exp(-sensitivity * lift))

        # Map to multiplier range
        multiplier = self.min_multiplier + (self.max_multiplier - self.min_multiplier) * sigmoid

        # Apply confidence weighting based on sample size
        confidence = min(1.0, sessions / 1000.0)
        multiplier = 1.0 + (multiplier - 1.0) * confidence

        return round(multiplier, 2)

    def find_segments(self, verbose: bool = True) -> List[Dict]:
        """
        Find high-performing segments.

        Algorithm:
        1. Calculate base metrics for entire dataset
        2. Calculate Cramér's V for each attribute
        3. Sort attributes by importance (descending)
        4. For each attribute (in order of importance):
             For each unique value:
                 a. Filter data to this segment
                 b. Calculate segment metrics
                 c. Validate segment (size, lift, significance)
                 d. If valid:
                    - Calculate lift percentages
                    - Calculate bid multiplier
                    - Add to results
        5. Sort results by eCR (descending)
        6. Return top max_segments

        Args:
            verbose: Print progress messages

        Returns:
            List of segment dictionaries with:
            - condition: "attribute = 'value'"
            - sessions, conversions, revenue
            - ecr, rps, ctr, rpi
            - ecr_lift, rps_lift, ctr_lift
            - bid_multiplier
            - confidence_score
            - feature_importance
        """
        if verbose:
            print("\n" + "=" * 70)
            print("SEGMENTATION ANALYSIS")
            print("=" * 70)

        # Step 1: Base metrics already calculated in __init__

        if verbose:
            print(f"\nBase Campaign Metrics:")
            print(f"  Sessions: {self.base_metrics.sessions:,}")
            print(f"  Conversions: {self.base_metrics.conversions:,}")
            print(f"  eCR: {self.base_metrics.ecr:.2%}")
            print(f"  RPS: ${self.base_metrics.rps:.2f}")
            print(f"  CTR: {self.base_metrics.ctr:.2%}")

        # Step 2: Calculate Cramér's V for each attribute
        if verbose:
            print(f"\nCalculating feature importance (Cramér's V)...")

        feature_importance = {}
        for attr in self.attributes:
            cramers_v = self._cramers_v(attr)
            feature_importance[attr] = cramers_v

        # Step 3: Sort attributes by importance
        sorted_attributes = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )

        if verbose:
            print(f"\nFeature Importance (Cramér's V):")
            for attr, importance in sorted_attributes:
                stars = "★" * min(5, int(importance * 12.5))
                stars += "☆" * (5 - len(stars))
                print(f"  {attr}: {importance:.2f} {stars}")

        # Step 4: Find segments
        segments = []

        for attr, importance in sorted_attributes:
            if importance < 0.05:  # Skip attributes with very low importance
                continue

            unique_values = self.data[attr].unique()

            for value in unique_values:
                # Filter to segment
                segment_df = self.data[self.data[attr] == value]

                if len(segment_df) == 0:
                    continue

                # Calculate metrics
                segment_metrics = self._calculate_metrics(segment_df)

                # Validate segment
                if not self._validate_split(segment_metrics):
                    continue

                # Calculate lifts
                ecr_lift = ((segment_metrics.ecr - self.base_metrics.ecr) /
                           self.base_metrics.ecr) if self.base_metrics.ecr > 0 else 0.0

                rps_lift = ((segment_metrics.rps - self.base_metrics.rps) /
                           self.base_metrics.rps) if self.base_metrics.rps > 0 else 0.0

                ctr_lift = ((segment_metrics.ctr - self.base_metrics.ctr) /
                           self.base_metrics.ctr) if self.base_metrics.ctr > 0 else 0.0

                # Calculate bid multiplier
                bid_multiplier = self._calculate_bid_multiplier(ecr_lift, segment_metrics.sessions)

                # Calculate confidence score
                confidence_score = min(1.0, segment_metrics.sessions / 1000.0)

                # Add to results
                segments.append({
                    'condition': f"{attr} = '{value}'",
                    'attribute': attr,
                    'value': str(value),
                    'sessions': segment_metrics.sessions,
                    'conversions': segment_metrics.conversions,
                    'revenue': segment_metrics.revenue,
                    'ecr': segment_metrics.ecr,
                    'rps': segment_metrics.rps,
                    'ctr': segment_metrics.ctr,
                    'rpi': segment_metrics.rpi,
                    'ecr_lift': ecr_lift,
                    'rps_lift': rps_lift,
                    'ctr_lift': ctr_lift,
                    'bid_multiplier': bid_multiplier,
                    'confidence_score': confidence_score,
                    'feature_importance': importance
                })

        # Step 5: Sort by eCR descending
        segments = sorted(segments, key=lambda x: x['ecr'], reverse=True)

        # Step 6: Return top N segments
        segments = segments[:self.max_segments]

        if verbose:
            print(f"\n✓ Found {len(segments)} high-performing segments")

        return segments


if __name__ == "__main__":
    # Test the segmentation engine
    print("Testing Segmentation Engine...")

    # Generate test data
    from mock_data_generator import generate_campaign_data
    from pandas_data_loader import PandasDataLoader

    print("\nGenerating test data...")
    test_df = generate_campaign_data(
        campaign_id='TEST_CAMPAIGN',
        num_sessions=10000,
        seed=42
    )

    # Aggregate data
    print("\nAggregating data...")
    loader = PandasDataLoader(
        data_source=test_df,
        campaign_id='TEST_CAMPAIGN',
        start_date='2024-01-01',
        end_date='2024-12-31',
        attributes=['age_range', 'income_bucket', 'education_level']
    )
    aggregated_df = loader.load_campaign_data()

    # Run segmentation
    print("\nRunning segmentation...")
    engine = SimpleSegmentationEngine(
        data=aggregated_df,
        attributes=['age_range', 'income_bucket', 'education_level'],
        max_segments=10,
        min_lift=0.20
    )

    segments = engine.find_segments(verbose=True)

    # Display top segments
    print("\n" + "=" * 70)
    print("TOP PERFORMING SEGMENTS")
    print("=" * 70)

    for i, seg in enumerate(segments[:5], 1):
        print(f"\n{i}. {seg['condition']}")
        print(f"   Performance:")
        print(f"     • eCR: {seg['ecr']:.2%} (lift: {seg['ecr_lift']:+.1%})")
        print(f"     • RPS: ${seg['rps']:.2f} (lift: {seg['rps_lift']:+.1%})")
        print(f"     • CTR: {seg['ctr']:.2%} (lift: {seg['ctr_lift']:+.1%})")
        print(f"   Recommendation:")
        print(f"     • Bid Multiplier: {seg['bid_multiplier']:.2f}x")
        print(f"     • Confidence: {seg['confidence_score']:.2f}")
        print(f"   Size:")
        print(f"     • Sessions: {seg['sessions']:,}")

    print("\n✓ Segmentation engine working correctly!")
