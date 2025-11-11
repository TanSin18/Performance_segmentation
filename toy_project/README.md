# Audience Miner 2.0 - Toy Implementation

A complete working implementation of an audience segmentation system for digital advertising campaign optimization. This toy project runs locally without cloud dependencies.

## Overview

Audience Miner 2.0 automatically discovers high-performing audience segments and provides data-driven bid adjustment recommendations for digital advertising campaigns.

**Key Features:**
- 📊 Statistical segmentation with Cramér's V for feature importance
- ✅ Chi-square validation for statistical significance
- 🎯 Sigmoid-based bid multiplier recommendations
- ⚖️ Campaign comparison to find competitive advantages
- 🚀 Pure Python implementation (Pandas, NumPy, SciPy only)

## What's Different from Production

This is a **toy implementation** designed for learning and demonstration:

| Production | Toy Project |
|------------|-------------|
| Apache Spark on Databricks | Pandas DataFrames |
| Real campaign data | Synthetic generated data |
| Cloud infrastructure | Local execution |
| Millions of sessions | Thousands of sessions |
| Complex multi-level splits | Single-level segmentation |

## Quick Start

### Installation

```bash
# Clone or download the project
cd toy_project

# Install dependencies
pip install -r requirements.txt
```

### Run the Complete System

```bash
# Run the full analysis pipeline
python main.py
```

This will:
1. Generate synthetic campaign data for 2 campaigns
2. Run segmentation analysis on Campaign A
3. Compare Campaign A vs Campaign B
4. Save results to CSV files

**Expected output:**
- `campaign_a_data.csv` - Raw data for Campaign A (15,000 sessions)
- `campaign_b_data.csv` - Raw data for Campaign B (15,000 sessions)
- `segmentation_results.csv` - Top performing segments with bid recommendations
- `comparison_results.csv` - Competitive insights between campaigns

**Runtime:** < 30 seconds on typical laptop

### Run the Minimal Demo

For a quick demonstration of core concepts:

```bash
python minimal_audience_miner.py
```

This runs a simplified ~200-line version showing all key algorithms.

## Project Structure

```
toy_project/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── main.py                           # Main orchestration script
├── mock_data_generator.py            # Synthetic data generation
├── pandas_data_loader.py             # Data loading and aggregation
├── simple_segmentation_engine.py     # Core segmentation algorithm
├── simple_comparison_engine.py       # Campaign comparison
└── minimal_audience_miner.py         # Single-file minimal demo
```

## Core Algorithms

### 1. Cramér's V (Feature Importance)

Measures the association between demographic attributes and conversion outcomes.

**Formula:**
```
V = √(χ² / (n × min(r-1, c-1)))
```

**Interpretation:**
- 0.0-0.1: Negligible association
- 0.1-0.2: Weak association
- 0.2-0.4: Moderate association ⭐ (good for segmentation)
- 0.4+: Strong association ⭐⭐ (prioritize!)

**Usage:**
```python
from simple_segmentation_engine import SimpleSegmentationEngine

engine = SimpleSegmentationEngine(data, attributes)
# Automatically ranks features by Cramér's V
segments = engine.find_segments()
```

### 2. Statistical Validation (Chi-Square Test)

Ensures segments have statistically significant performance differences.

**Validation Criteria:**
1. **Minimum Size:** Segment ≥ 5% of total sessions
2. **Minimum Lift:** eCR lift ≥ 20%
3. **Statistical Significance:** Chi-square p-value < 0.05 (95% confidence)

**2×2 Contingency Table:**
```
                  Converted | Not Converted
Segment           a         | b
Baseline          c         | d
```

### 3. Sigmoid Bid Multiplier

Transforms performance lift into bid adjustment recommendations.

**Formula:**
```python
sigmoid = 1 / (1 + exp(-5 × lift))
multiplier = 0.70 + (1.50 - 0.70) × sigmoid
confidence = min(1.0, sessions / 1000)
multiplier = 1.0 + (multiplier - 1.0) × confidence
```

**Examples:**
- **+50% lift, 10,000 sessions** → 1.44x multiplier (increase bids 44%)
- **+20% lift, 2,000 sessions** → 1.28x multiplier (increase bids 28%)
- **0% lift** → 1.00x (no change)
- **-20% lift, 2,000 sessions** → 0.82x (decrease bids 18%)

**Confidence Weighting:**
Smaller segments get conservative multipliers to account for uncertainty.

## Usage Examples

### Example 1: Basic Segmentation

```python
from mock_data_generator import generate_campaign_data
from pandas_data_loader import PandasDataLoader
from simple_segmentation_engine import SimpleSegmentationEngine

# Generate data
data = generate_campaign_data('MY_CAMPAIGN', num_sessions=10000)

# Load and aggregate
loader = PandasDataLoader(
    data_source=data,
    campaign_id='MY_CAMPAIGN',
    start_date='2024-01-01',
    end_date='2024-12-31',
    attributes=['age_range', 'income_bucket']
)
aggregated = loader.load_campaign_data()

# Find segments
engine = SimpleSegmentationEngine(
    data=aggregated,
    attributes=['age_range', 'income_bucket'],
    max_segments=10,
    min_lift=0.20
)
segments = engine.find_segments()

# Display results
for seg in segments[:3]:
    print(f"{seg['condition']}")
    print(f"  eCR: {seg['ecr']:.2%} (lift: {seg['ecr_lift']:+.1%})")
    print(f"  Bid Multiplier: {seg['bid_multiplier']:.2f}x")
```

### Example 2: Campaign Comparison

```python
from simple_comparison_engine import SimpleComparisonEngine

# Compare two campaigns
engine = SimpleComparisonEngine(
    data_a=aggregated_campaign_a,
    data_b=aggregated_campaign_b,
    campaign_a_id='Campaign_A',
    campaign_b_id='Campaign_B',
    attributes=['age_range', 'income_bucket'],
    min_advantage=0.20
)
comparisons = engine.compare()

# Display advantages
for comp in comparisons[:3]:
    print(f"{comp['segment_condition']}")
    print(f"  Advantage: {comp['overall_advantage']}")
    print(f"  A eCR: {comp['campaign_a_ecr']:.2%}")
    print(f"  B eCR: {comp['campaign_b_ecr']:.2%}")
```

### Example 3: Custom Configuration

```python
# More aggressive segmentation
engine = SimpleSegmentationEngine(
    data=aggregated,
    attributes=['age_range', 'income_bucket', 'education_level'],
    max_segments=20,           # Find more segments
    min_lift=0.15,            # Lower lift threshold (15%)
    min_segment_pct=0.03,     # Smaller segments (3% of total)
    significance_threshold=0.10,  # Less strict p-value
    min_multiplier=0.60,      # Wider multiplier range
    max_multiplier=1.80
)
segments = engine.find_segments()
```

## Output Format

### Segmentation Results CSV

| Column | Description | Example |
|--------|-------------|---------|
| condition | Segment definition | `income_bucket = '100K+'` |
| attribute | Attribute name | `income_bucket` |
| value | Attribute value | `100K+` |
| sessions | Number of sessions | `1,800` |
| conversions | Number of conversions | `74` |
| ecr | Engagement conversion rate | `0.0411` (4.11%) |
| rps | Revenue per session | `1.35` |
| ctr | Click-through rate | `0.045` (4.5%) |
| ecr_lift | eCR lift vs baseline | `0.648` (+64.8%) |
| rps_lift | RPS lift vs baseline | `0.588` (+58.8%) |
| ctr_lift | CTR lift vs baseline | `0.423` (+42.3%) |
| bid_multiplier | Recommended multiplier | `1.42` |
| confidence_score | Confidence (0-1) | `0.95` |
| feature_importance | Cramér's V | `0.45` |

### Comparison Results CSV

| Column | Description | Example |
|--------|-------------|---------|
| segment_condition | Segment definition | `income_bucket = '100K+'` |
| overall_advantage | Which campaign wins | `Strong Campaign_A Advantage` |
| campaign_a_ecr | Campaign A eCR | `0.0412` (4.12%) |
| campaign_b_ecr | Campaign B eCR | `0.0301` (3.01%) |
| ecr_diff_pct | eCR difference | `0.369` (+36.9%) |
| campaign_a_rps | Campaign A RPS | `1.35` |
| campaign_b_rps | Campaign B RPS | `0.95` |
| rps_diff_pct | RPS difference | `0.421` (+42.1%) |

## Configuration Options

### Segmentation Parameters

- **max_segments** (default: 10): Maximum number of segments to return
- **min_lift** (default: 0.20): Minimum performance lift required (20%)
- **min_segment_pct** (default: 0.05): Minimum segment size (5% of total)
- **significance_threshold** (default: 0.05): P-value threshold (0.05 = 95% confidence)
- **min_multiplier** (default: 0.70): Minimum bid multiplier (70%)
- **max_multiplier** (default: 1.50): Maximum bid multiplier (150%)

### Comparison Parameters

- **min_advantage** (default: 0.20): Minimum difference to highlight (20%)
- **min_sessions** (default: 100): Minimum sessions per segment

## Extending the Project

### Add New Attributes

Edit `mock_data_generator.py` to add new demographic attributes:

```python
# Add new attribute
data['region'] = np.random.choice(['North', 'South', 'East', 'West'], num_sessions)

# Add performance multiplier
region_multipliers = {
    'North': 1.1,
    'South': 0.9,
    'East': 1.2,
    'West': 1.0
}
df['performance_multiplier'] *= df['region'].map(region_multipliers)
```

Then include it in analysis:

```python
attributes = ['age_range', 'income_bucket', 'region']  # Add 'region'
```

### Add Visualization

```python
import matplotlib.pyplot as plt

# Plot segment performance
segments_df = pd.DataFrame(segments)
plt.figure(figsize=(10, 6))
plt.barh(segments_df['condition'], segments_df['ecr_lift'])
plt.xlabel('eCR Lift')
plt.title('Top Performing Segments')
plt.tight_layout()
plt.savefig('segments_performance.png')
```

### Export to JSON

```python
import json

# Save as JSON
with open('segments.json', 'w') as f:
    json.dump(segments, f, indent=2)
```

### Multi-Level Segmentation

Implement recursive splitting for compound conditions:

```python
# Example: "income='100K+' AND age='35-44'"
# This requires modifying the segmentation engine to:
# 1. Find best single-attribute segments
# 2. For each segment, recursively split on other attributes
# 3. Validate each sub-segment
```

## Troubleshooting

### Issue: No segments found

**Causes:**
- `min_lift` threshold too high
- `min_segment_pct` too large
- Data lacks performance variance

**Solutions:**
- Lower `min_lift` to 0.15 or 0.10
- Reduce `min_segment_pct` to 0.03
- Generate more diverse data (adjust performance multipliers)

### Issue: All segments have low Cramér's V

**Cause:** Attributes don't correlate with conversions

**Solution:** Check performance multipliers in `mock_data_generator.py`

### Issue: RuntimeWarning: divide by zero

**Cause:** Some segments have zero impressions or sessions

**Solution:** Add filters in data loader:

```python
aggregated = aggregated[aggregated['impressions'] > 0]
aggregated = aggregated[aggregated['viewed_sessions'] > 0]
```

### Issue: Chi-square test fails

**Cause:** Contingency table has zero or negative values

**Solution:** This is handled automatically by validation - segments that fail are skipped

## Performance Notes

**Expected Performance:**
- 15,000 sessions: ~20-30 seconds
- 50,000 sessions: ~60-90 seconds
- 100,000+ sessions: Consider sampling

**Optimization Tips:**
- Use fewer attributes (3-4 max)
- Pre-filter data by date range or source
- Use `min_segment_pct=0.05` or higher to skip tiny segments
- Cache aggregated data for multiple analyses

## Testing

Run individual component tests:

```bash
# Test data generator
python mock_data_generator.py

# Test data loader
python pandas_data_loader.py

# Test segmentation engine
python simple_segmentation_engine.py

# Test comparison engine
python simple_comparison_engine.py

# Test minimal version
python minimal_audience_miner.py

# Test full system
python main.py
```

## Key Metrics Explained

### eCR (Engagement Conversion Rate)
```
eCR = conversions / viewed_sessions
```
Percentage of engaged sessions that convert.

### RPS (Revenue Per Session)
```
RPS = revenue / viewed_sessions
```
Average revenue per engaged session.

### CTR (Click-Through Rate)
```
CTR = clicks / impressions
```
Percentage of impressions that result in clicks.

### RPI (Revenue Per Impression)
```
RPI = revenue / impressions
```
Average revenue per impression.

## References

- **Cramér's V:** [Wikipedia](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V)
- **Chi-Square Test:** [SciPy Documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html)
- **Sigmoid Function:** [Wikipedia](https://en.wikipedia.org/wiki/Sigmoid_function)

## License

This is a toy project for educational purposes. Use at your own risk.

## Support

For questions or issues, please review the code comments and docstrings. All functions have detailed documentation.

## Success Criteria

The implementation is complete when:

✅ `python main.py` runs without errors
✅ Generates 4 output CSV files
✅ Finds 8-10 high-performing segments
✅ Top segment has eCR lift ≥ 40%
✅ Cramér's V correctly ranks features
✅ Bid multipliers in valid range [0.70, 1.50]
✅ Campaign comparison finds advantages
✅ All statistical tests work correctly
✅ Runtime < 30 seconds on typical laptop

---

**Built with:** Python 3.7+, Pandas, NumPy, SciPy

**Author:** Audience Miner 2.0 Toy Project

**Version:** 1.0.0
