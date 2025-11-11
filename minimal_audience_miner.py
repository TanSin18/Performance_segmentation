"""
Minimal Audience Miner - Single File Demo

A simplified ~200-line implementation demonstrating core concepts:
- Synthetic data generation
- Cramér's V for feature importance
- Statistical segmentation
- Sigmoid bid multipliers
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency


# ============================================================================
# 1. DATA GENERATION
# ============================================================================

def generate_data(num_rows=5000, seed=42):
    """Generate synthetic campaign data."""
    np.random.seed(seed)

    # Demographics
    age_ranges = ['18-24', '25-34', '35-44', '45-54', '55+']
    income_buckets = ['<50K', '50-75K', '75-100K', '100K+']
    education_levels = ['High School', 'Bachelor', 'Graduate']

    data = {
        'age_range': np.random.choice(age_ranges, num_rows),
        'income_bucket': np.random.choice(income_buckets, num_rows),
        'education_level': np.random.choice(education_levels, num_rows),
    }

    df = pd.DataFrame(data)

    # Performance multipliers
    multiplier = np.ones(num_rows)
    multiplier *= df['income_bucket'].map({
        '<50K': 0.9, '50-75K': 1.0, '75-100K': 1.2, '100K+': 1.5
    })
    multiplier *= df['education_level'].map({
        'High School': 0.9, 'Bachelor': 1.0, 'Graduate': 1.3
    })
    multiplier *= df['age_range'].map({
        '18-24': 0.85, '25-34': 1.0, '35-44': 1.25, '45-54': 1.2, '55+': 1.0
    })

    # Generate metrics
    df['viewed_sessions'] = 1
    df['impressions'] = np.random.randint(1, 20, num_rows)

    # Generate clicks based on CTR
    base_ctr = np.random.uniform(0.02, 0.06, num_rows)
    adjusted_ctr = base_ctr * multiplier
    adjusted_ctr = np.clip(adjusted_ctr, 0, 0.15)
    df['clicks'] = np.random.binomial(df['impressions'], adjusted_ctr)

    # Generate conversions based on eCR
    base_ecr = np.random.uniform(0.01, 0.04, num_rows)
    adjusted_ecr = base_ecr * multiplier
    adjusted_ecr = np.clip(adjusted_ecr, 0, 0.12)
    df['conversions'] = np.random.binomial(1, adjusted_ecr)

    # Generate revenue
    df['revenue'] = df['conversions'] * np.random.uniform(20, 60, num_rows)

    return df


# ============================================================================
# 2. AGGREGATION
# ============================================================================

def aggregate_data(df, attributes):
    """Aggregate data by attributes."""
    return df.groupby(attributes, as_index=False).agg({
        'viewed_sessions': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'revenue': 'sum'
    })


# ============================================================================
# 3. METRICS
# ============================================================================

def calculate_metrics(df):
    """Calculate performance metrics."""
    sessions = df['viewed_sessions'].sum()
    conversions = df['conversions'].sum()
    revenue = df['revenue'].sum()
    impressions = df['impressions'].sum()
    clicks = df['clicks'].sum()

    ecr = conversions / sessions if sessions > 0 else 0
    rps = revenue / sessions if sessions > 0 else 0
    ctr = clicks / impressions if impressions > 0 else 0

    return {
        'sessions': sessions,
        'conversions': conversions,
        'revenue': revenue,
        'ecr': ecr,
        'rps': rps,
        'ctr': ctr
    }


# ============================================================================
# 4. CRAMÉR'S V (Feature Importance)
# ============================================================================

def calculate_cramers_v(df, attribute):
    """
    Calculate Cramér's V for feature importance.

    Measures association between attribute and conversion.
    Range: 0.0 (no association) to 1.0 (perfect association)
    """
    try:
        # Create contingency table
        contingency = pd.crosstab(
            df[attribute],
            df['conversions'] > 0
        )

        # Chi-square test
        chi2, p_value, dof, expected = chi2_contingency(contingency)

        # Calculate Cramér's V
        n = contingency.sum().sum()
        min_dim = min(contingency.shape[0] - 1, contingency.shape[1] - 1)

        if n > 0 and min_dim > 0:
            return np.sqrt(chi2 / (n * min_dim))
        return 0.0
    except:
        return 0.0


# ============================================================================
# 5. SEGMENTATION
# ============================================================================

def find_segments(df, attributes, max_segments=10, min_lift=0.20):
    """
    Find high-performing segments.

    Algorithm:
    1. Calculate base metrics
    2. Rank attributes by Cramér's V
    3. Find segments with lift >= min_lift
    4. Calculate sigmoid bid multipliers
    5. Return top segments by eCR
    """
    # Base metrics
    base = calculate_metrics(df)

    print(f"\nBase Metrics:")
    print(f"  Sessions: {base['sessions']:,}")
    print(f"  eCR: {base['ecr']:.2%}")
    print(f"  RPS: ${base['rps']:.2f}")

    # Feature importance
    print(f"\nFeature Importance (Cramér's V):")
    importance = {}
    for attr in attributes:
        v = calculate_cramers_v(df, attr)
        importance[attr] = v
        stars = "★" * int(v * 20) + "☆" * (5 - int(v * 20))
        print(f"  {attr}: {v:.3f} {stars}")

    # Find segments
    segments = []
    sorted_attrs = sorted(importance.items(), key=lambda x: x[1], reverse=True)

    for attr, imp in sorted_attrs:
        for value in df[attr].unique():
            segment_df = df[df[attr] == value]
            seg_metrics = calculate_metrics(segment_df)

            # Check minimum size (5% of total)
            if seg_metrics['sessions'] < base['sessions'] * 0.05:
                continue

            # Calculate lift
            ecr_lift = (seg_metrics['ecr'] - base['ecr']) / base['ecr'] if base['ecr'] > 0 else 0
            rps_lift = (seg_metrics['rps'] - base['rps']) / base['rps'] if base['rps'] > 0 else 0

            # Check minimum lift
            if ecr_lift < min_lift:
                continue

            # Calculate sigmoid bid multiplier
            sensitivity = 5.0
            sigmoid = 1.0 / (1.0 + np.exp(-sensitivity * ecr_lift))
            multiplier = 0.70 + (1.50 - 0.70) * sigmoid
            confidence = min(1.0, seg_metrics['sessions'] / 1000.0)
            multiplier = 1.0 + (multiplier - 1.0) * confidence

            segments.append({
                'condition': f"{attr} = '{value}'",
                'sessions': seg_metrics['sessions'],
                'conversions': seg_metrics['conversions'],
                'ecr': seg_metrics['ecr'],
                'rps': seg_metrics['rps'],
                'ecr_lift': ecr_lift,
                'rps_lift': rps_lift,
                'bid_multiplier': round(multiplier, 2),
                'confidence': round(confidence, 2)
            })

    # Sort by eCR and return top N
    segments = sorted(segments, key=lambda x: x['ecr'], reverse=True)
    return segments[:max_segments]


# ============================================================================
# 6. MAIN
# ============================================================================

def main():
    """Main execution function."""
    print("=" * 70)
    print("MINIMAL AUDIENCE MINER - DEMO")
    print("=" * 70)

    # Generate data
    print("\n1. Generating synthetic data...")
    df = generate_data(num_rows=8000, seed=42)
    print(f"   ✓ Generated {len(df):,} sessions")

    # Aggregate
    print("\n2. Aggregating data...")
    attributes = ['age_range', 'income_bucket', 'education_level']
    agg_df = aggregate_data(df, attributes)
    print(f"   ✓ Aggregated to {len(agg_df):,} segments")

    # Find segments
    print("\n3. Finding high-performing segments...")
    segments = find_segments(agg_df, attributes, max_segments=10, min_lift=0.20)

    # Display results
    print("\n" + "=" * 70)
    print(f"TOP {len(segments)} PERFORMING SEGMENTS")
    print("=" * 70)

    for i, seg in enumerate(segments, 1):
        print(f"\n{i}. {seg['condition']}")
        print(f"   Performance:")
        print(f"     • eCR: {seg['ecr']:.2%} (lift: {seg['ecr_lift']:+.1%})")
        print(f"     • RPS: ${seg['rps']:.2f} (lift: {seg['rps_lift']:+.1%})")
        print(f"   Recommendation:")
        print(f"     • Bid Multiplier: {seg['bid_multiplier']:.2f}x")
        print(f"     • Confidence: {seg['confidence']:.2f}")
        print(f"   Size: {seg['sessions']:,} sessions")

    # Save to CSV
    print("\n" + "=" * 70)
    print("SAVING RESULTS")
    print("=" * 70)

    results_df = pd.DataFrame(segments)
    results_df.to_csv('minimal_segments.csv', index=False)
    print(f"✓ Saved results to minimal_segments.csv")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ Found {len(segments)} high-performing segments")

    if len(segments) > 0:
        print(f"✓ Top segment has {segments[0]['ecr_lift']:.1%} eCR lift")
        print(f"✓ Recommended bid multipliers range: "
              f"{min(s['bid_multiplier'] for s in segments):.2f}x - "
              f"{max(s['bid_multiplier'] for s in segments):.2f}x")
    else:
        print("! No segments met the criteria (try lowering min_lift or min_segment_pct)")

    print("\n✓ Analysis complete!\n")


if __name__ == "__main__":
    main()
