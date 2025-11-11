"""
Main Orchestration Script for Audience Miner 2.0 Toy Project

Complete working example that ties all components together.
"""

import pandas as pd
from typing import List
import time

from mock_data_generator import generate_campaign_data, save_mock_data
from pandas_data_loader import PandasDataLoader
from simple_segmentation_engine import SimpleSegmentationEngine
from simple_comparison_engine import SimpleComparisonEngine


def print_header():
    """Print application header."""
    print("\n" + "=" * 70)
    print(" " * 15 + "AUDIENCE MINER 2.0 - TOY PROJECT")
    print("=" * 70)
    print("\nA complete working implementation of audience segmentation")
    print("for digital advertising campaign optimization.")
    print("\nFeatures:")
    print("  • Statistical segmentation with Cramér's V")
    print("  • Chi-square validation")
    print("  • Sigmoid bid multipliers")
    print("  • Campaign comparison analysis")
    print("=" * 70 + "\n")


def display_top_segments(segments: List[dict], num_to_show: int = 5):
    """Display top performing segments."""
    print("\n" + "=" * 70)
    print("TOP PERFORMING SEGMENTS")
    print("=" * 70)

    for i, seg in enumerate(segments[:num_to_show], 1):
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
        print(f"     • Conversions: {seg['conversions']:,}")
        print(f"     • Revenue: ${seg['revenue']:.2f}")


def display_top_comparisons(comparisons: List[dict], num_to_show: int = 5):
    """Display top competitive insights."""
    print("\n" + "=" * 70)
    print("TOP COMPETITIVE INSIGHTS")
    print("=" * 70)

    for i, comp in enumerate(comparisons[:num_to_show], 1):
        print(f"\n{i}. {comp['segment_condition']}")
        print(f"   Advantage: {comp['overall_advantage']}")
        print(f"   Campaign A:")
        print(f"     • eCR: {comp['campaign_a_ecr']:.2%}")
        print(f"     • RPS: ${comp['campaign_a_rps']:.2f}")
        print(f"     • CTR: {comp['campaign_a_ctr']:.2%}")
        print(f"   Campaign B:")
        print(f"     • eCR: {comp['campaign_b_ecr']:.2%}")
        print(f"     • RPS: ${comp['campaign_b_rps']:.2f}")
        print(f"     • CTR: {comp['campaign_b_ctr']:.2%}")
        print(f"   Differences:")
        print(f"     • eCR: {comp['ecr_diff_pct']:+.1%}")
        print(f"     • RPS: {comp['rps_diff_pct']:+.1%}")
        print(f"     • CTR: {comp['ctr_diff_pct']:+.1%}")


def save_segmentation_results(segments: List[dict], filename: str = 'segmentation_results.csv'):
    """Save segmentation results to CSV."""
    df = pd.DataFrame(segments)

    # Select and order columns for output
    output_columns = [
        'condition', 'attribute', 'value', 'sessions', 'conversions', 'revenue',
        'ecr', 'rps', 'ctr', 'ecr_lift', 'rps_lift', 'ctr_lift',
        'bid_multiplier', 'confidence_score', 'feature_importance'
    ]

    # Only include columns that exist
    output_columns = [col for col in output_columns if col in df.columns]

    df[output_columns].to_csv(filename, index=False)
    print(f"✓ Saved segmentation results to {filename}")


def save_comparison_results(comparisons: List[dict], filename: str = 'comparison_results.csv'):
    """Save comparison results to CSV."""
    df = pd.DataFrame(comparisons)

    # Select and order columns for output
    output_columns = [
        'segment_condition', 'attribute', 'value', 'overall_advantage',
        'campaign_a_sessions', 'campaign_b_sessions',
        'campaign_a_ecr', 'campaign_b_ecr', 'ecr_diff_pct',
        'campaign_a_rps', 'campaign_b_rps', 'rps_diff_pct',
        'campaign_a_ctr', 'campaign_b_ctr', 'ctr_diff_pct',
        'ecr_advantage', 'rps_advantage', 'ctr_advantage'
    ]

    # Only include columns that exist
    output_columns = [col for col in output_columns if col in df.columns]

    df[output_columns].to_csv(filename, index=False)
    print(f"✓ Saved comparison results to {filename}")


def main():
    """
    Main execution function.

    Process:
    1. Print header
    2. Generate mock data for 2 campaigns
    3. Save to CSV files
    4. Load and aggregate campaign A data
    5. Run segmentation analysis on campaign A
    6. Display top 5 segments
    7. Save segmentation results to CSV
    8. Load campaign B data
    9. Run comparison between A and B
    10. Display top 5 comparative insights
    11. Save comparison results to CSV
    12. Print summary

    Output Files:
    - campaign_a_data.csv: Raw data
    - campaign_b_data.csv: Raw data
    - segmentation_results.csv: Segment recommendations
    - comparison_results.csv: Competitive insights
    """
    start_time = time.time()

    # Step 1: Print header
    print_header()

    # Step 2-3: Generate mock data for 2 campaigns
    print("STEP 1: Generating Mock Data")
    print("-" * 70)

    print("\nGenerating Campaign A data...")
    campaign_a_data = generate_campaign_data(
        campaign_id='CAMPAIGN_A',
        num_sessions=15000,
        start_date='2024-01-01',
        end_date='2024-12-31',
        seed=42
    )
    campaign_a_data.to_csv('campaign_a_data.csv', index=False)
    print(f"✓ Generated {len(campaign_a_data):,} sessions for Campaign A")

    print("\nGenerating Campaign B data...")
    campaign_b_data = generate_campaign_data(
        campaign_id='CAMPAIGN_B',
        num_sessions=15000,
        start_date='2024-01-01',
        end_date='2024-12-31',
        seed=123
    )
    campaign_b_data.to_csv('campaign_b_data.csv', index=False)
    print(f"✓ Generated {len(campaign_b_data):,} sessions for Campaign B")

    # Step 4-5: Load and aggregate campaign A data
    print("\n" + "=" * 70)
    print("STEP 2: Running Segmentation Analysis on Campaign A")
    print("-" * 70)

    attributes = ['age_range', 'income_bucket', 'education_level', 'net_asset_value']

    print("\nLoading and aggregating Campaign A data...")
    loader_a = PandasDataLoader(
        data_source='campaign_a_data.csv',
        campaign_id='CAMPAIGN_A',
        start_date='2024-01-01',
        end_date='2024-12-31',
        attributes=attributes
    )
    aggregated_a = loader_a.load_campaign_data()

    # Step 6: Run segmentation analysis
    print("\nRunning segmentation engine...")
    segmentation_engine = SimpleSegmentationEngine(
        data=aggregated_a,
        attributes=attributes,
        max_segments=10,
        min_lift=0.20,
        min_segment_pct=0.05,
        significance_threshold=0.05
    )

    segments = segmentation_engine.find_segments(verbose=True)

    # Step 7: Display top 5 segments
    display_top_segments(segments, num_to_show=5)

    # Step 8: Save segmentation results
    print("\n" + "-" * 70)
    save_segmentation_results(segments, 'segmentation_results.csv')

    # Step 9-10: Load campaign B and run comparison
    print("\n" + "=" * 70)
    print("STEP 3: Comparing Campaign A vs Campaign B")
    print("-" * 70)

    print("\nLoading and aggregating Campaign B data...")
    loader_b = PandasDataLoader(
        data_source='campaign_b_data.csv',
        campaign_id='CAMPAIGN_B',
        start_date='2024-01-01',
        end_date='2024-12-31',
        attributes=attributes
    )
    aggregated_b = loader_b.load_campaign_data()

    # Step 11: Run comparison
    print("\nRunning comparison engine...")
    comparison_engine = SimpleComparisonEngine(
        data_a=aggregated_a,
        data_b=aggregated_b,
        campaign_a_id='Campaign_A',
        campaign_b_id='Campaign_B',
        attributes=attributes,
        min_advantage=0.20,
        min_sessions=100
    )

    comparisons = comparison_engine.compare(verbose=True)

    # Step 12: Display top 5 comparisons
    display_top_comparisons(comparisons, num_to_show=5)

    # Step 13: Save comparison results
    print("\n" + "-" * 70)
    save_comparison_results(comparisons, 'comparison_results.csv')

    # Step 14: Print summary
    elapsed_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"\n✓ Analysis Complete!")
    print(f"✓ Found {len(segments)} high-performing segments")

    if len(segments) > 0:
        top_segment = segments[0]
        print(f"✓ Top segment: {top_segment['condition']}")
        print(f"  - eCR lift: {top_segment['ecr_lift']:.1%}")
        print(f"  - Bid multiplier: {top_segment['bid_multiplier']:.2f}x")

    # Count advantages
    a_advantages = sum(1 for c in comparisons if 'Campaign_A' in c['overall_advantage'])
    b_advantages = sum(1 for c in comparisons if 'Campaign_B' in c['overall_advantage'])

    print(f"\n✓ Campaign A has advantage in {a_advantages} segments")
    print(f"✓ Campaign B has advantage in {b_advantages} segments")

    print(f"\nOutput Files:")
    print(f"  1. campaign_a_data.csv ({len(campaign_a_data):,} rows)")
    print(f"  2. campaign_b_data.csv ({len(campaign_b_data):,} rows)")
    print(f"  3. segmentation_results.csv ({len(segments)} segments)")
    print(f"  4. comparison_results.csv ({len(comparisons)} comparisons)")

    print(f"\nExecution Time: {elapsed_time:.2f} seconds")

    print("\n" + "=" * 70)
    print("✓ ALL DONE!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
