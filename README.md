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

---

## 🤖 AI Agent (NEW!)

**Audience Miner 2.0 now includes an AI agent** that uses natural language to analyze campaigns and provide intelligent recommendations.

### What is the AI Agent?

The AI agent uses **ReAct (Reasoning + Acting)** architecture to:
- Understand natural language queries
- Autonomously use analysis tools
- Reason about campaign performance
- Provide actionable, data-driven recommendations
- Explain its reasoning step-by-step

### Quick Start with the Agent

#### 1. Setup API Key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API key
# For OpenAI (recommended for quick start):
echo "OPENAI_API_KEY=your_key_here" >> .env

# Or for Anthropic Claude:
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

Get API keys:
- **OpenAI**: https://platform.openai.com/api-keys (Recommended: gpt-4o-mini is fast and cheap)
- **Anthropic**: https://console.anthropic.com/

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run the Agent

**Interactive Mode** (Best experience):
```bash
python agent_cli.py
```

**Single Query Mode**:
```bash
python agent_cli.py --query "Analyze Campaign_A and show top segments"
```

**Demo Mode**:
```bash
python agent_cli.py --demo
```

### Example Agent Conversations

```
You: Analyze Campaign_A and find the best opportunities

🤖 Agent: I'll analyze Campaign_A for you. Let me start by loading the data...

[Agent loads data, runs segmentation, validates results]

🤖 Agent: I found 8 high-performing segments. Here are the top 3:

1. INCREASE BIDS for income_bucket = '100K+'
   Current eCR: 4.11% (baseline lift: +64.8%)
   Recommended bid adjustment: +42% (multiplier: 1.42x)
   Segment size: 1,800 sessions
   Confidence: 95%

2. INCREASE BIDS for age_range = '35-44'
   Current eCR: 3.85% (baseline lift: +54.2%)
   Recommended bid adjustment: +38% (multiplier: 1.38x)
   Segment size: 2,100 sessions
   Confidence: 98%

3. INCREASE BIDS for education_level = 'Graduate'
   Current eCR: 3.65% (baseline lift: +46.3%)
   Recommended bid adjustment: +34% (multiplier: 1.34x)
   Segment size: 1,650 sessions
   Confidence: 92%

These recommendations are statistically significant (p < 0.05) and should
increase your campaign ROI by an estimated 25-35%.
```

```
You: Compare Campaign_A and Campaign_B

🤖 Agent: Let me load both campaigns and compare their performance...

[Agent loads and analyzes both campaigns]

🤖 Agent: Campaign_A has a strong advantage in 3 key segments:

1. income_bucket = '100K+': Campaign_A eCR is 4.11% vs Campaign_B's 3.01%
   (+36.9% advantage). You're winning affluent audiences!

2. age_range = '35-44': Campaign_A eCR is 3.85% vs Campaign_B's 2.95%
   (+30.5% advantage). Your creative resonates better with this age group.

3. device_type = 'Desktop': Campaign_A eCR is 3.25% vs Campaign_B's 2.80%
   (+16.1% advantage). Desktop experience is superior.

Recommendation: Double down on high-income, 35-44 age, desktop users for
Campaign_A. Consider improving Campaign_B's creative for these segments.
```

### Agent CLI Commands

**Quick Commands**:
```bash
analyze <campaign_id>              # Analyze campaign
compare <campaign_a> <campaign_b>  # Compare campaigns
segments <campaign_id>             # Show top segments
list                               # List loaded campaigns
help                               # Show help
exit                               # Quit
```

**Natural Language Queries** (just type what you want):
```
"Which segments should I bid higher on?"
"What's the ROI impact of the top segment?"
"Show me segments with at least 50% lift"
"Give me 5 actionable recommendations"
"Why is Campaign_B underperforming?"
"Calculate potential revenue increase for the best segment"
```

### Agent CLI Options

```bash
# Use different LLM providers
python agent_cli.py --provider openai    # OpenAI GPT (default)
python agent_cli.py --provider anthropic # Anthropic Claude
python agent_cli.py --provider ollama    # Local Ollama

# Use specific models
python agent_cli.py --model gpt-4              # More powerful
python agent_cli.py --model claude-3-5-sonnet-20241022  # Claude Sonnet

# Hide reasoning steps (faster output)
python agent_cli.py --no-verbose

# Single query without interactive mode
python agent_cli.py -q "Analyze Campaign_A"
```

### Using Local LLMs (Ollama)

**No API key required!** Run models locally:

```bash
# 1. Install Ollama
# Visit: https://ollama.ai

# 2. Download a model
ollama pull llama3

# 3. Run the agent with Ollama
python agent_cli.py --provider ollama --model llama3
```

### Programmatic Usage

```python
from react_agent import create_agent

# Create agent
agent = create_agent(
    provider='openai',
    model='gpt-4o-mini',
    verbose=True
)

# Ask questions
response = agent.chat("What are the best segments for Campaign_A?")
print(response)

# Run multiple queries
queries = [
    "Load Campaign_A",
    "Show me top 5 segments",
    "Calculate ROI for the best segment"
]

for query in queries:
    response = agent.chat(query)
    print(f"Q: {query}\nA: {response}\n")
```

### How the Agent Works

The agent uses **ReAct (Reasoning + Acting)** architecture:

1. **Reasoning**: Agent thinks about the problem
   - "I need to load campaign data first"
   - "I should validate statistical significance"
   - "I should explain the impact in business terms"

2. **Acting**: Agent uses tools to gather information
   - `load_campaign_data(campaign_id)`
   - `run_segmentation_analysis(campaign_id)`
   - `calculate_roi_impact(segment)`

3. **Observing**: Agent sees results and adjusts
   - Reads tool outputs
   - Validates findings
   - Synthesizes insights

4. **Responding**: Agent provides comprehensive answer
   - Data-driven recommendations
   - Clear explanations
   - Actionable next steps

### Available Agent Tools

The agent can use these tools autonomously:

| Tool | Purpose |
|------|---------|
| `load_campaign_data` | Load and summarize campaign metrics |
| `run_segmentation_analysis` | Find high-performing segments |
| `compare_campaigns` | Compare two campaigns |
| `get_segment_details` | Deep dive on specific segment |
| `calculate_roi_impact` | Project ROI of optimizations |
| `list_campaigns` | Show loaded campaigns |
| `get_recommendations` | Get actionable summary |

### Agent Configuration

Edit `.env` or `agent_config.py` to customize:

```python
# LLM Settings
AGENT_PROVIDER=openai           # openai, anthropic, ollama
AGENT_MODEL=gpt-4o-mini        # model name
AGENT_VERBOSE=true             # show reasoning

# Analysis Defaults
DEFAULT_MAX_SEGMENTS=10        # max segments to find
DEFAULT_MIN_LIFT=0.20          # minimum lift (20%)
DEFAULT_MIN_SEGMENT_PCT=0.05   # minimum size (5%)
```

### Cost Estimates

**OpenAI GPT-4o-mini** (Recommended):
- ~$0.01-0.05 per query
- Very fast responses
- High quality analysis

**OpenAI GPT-4**:
- ~$0.10-0.50 per query
- Best reasoning quality
- Slower but more thorough

**Anthropic Claude Sonnet**:
- ~$0.05-0.20 per query
- Excellent for complex analysis
- Strong at explanations

**Ollama (Local)**:
- Free!
- Requires GPU for good performance
- Privacy-friendly

### Troubleshooting

**"API key not found"**:
- Make sure `.env` file exists
- Check API key is correct
- Try: `export OPENAI_API_KEY='your-key'`

**"Rate limit exceeded"**:
- Wait a few seconds and retry
- Upgrade your API plan
- Use cheaper model (gpt-4o-mini)

**"Agent keeps failing"**:
- Enable verbose mode to see reasoning: `--verbose`
- Check if campaign data loaded correctly
- Try simpler query first

**Poor quality responses**:
- Try gpt-4 instead of gpt-4o-mini: `--model gpt-4`
- Be more specific in your query
- Enable verbose to see agent's thinking

---

### Run the Minimal Demo

For a quick demonstration of core concepts:

```bash
python minimal_audience_miner.py
```

This runs a simplified ~200-line version showing all key algorithms.

## Project Structure

```
Performance_segmentation/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
│
├── main.py                           # Main orchestration script
├── mock_data_generator.py            # Synthetic data generation
├── pandas_data_loader.py             # Data loading and aggregation
├── simple_segmentation_engine.py     # Core segmentation algorithm
├── simple_comparison_engine.py       # Campaign comparison
├── minimal_audience_miner.py         # Single-file minimal demo
│
├── agent_tools.py                    # 🤖 AI agent tool wrappers
├── react_agent.py                    # 🤖 ReAct agent implementation
├── agent_cli.py                      # 🤖 Interactive CLI interface
├── agent_config.py                   # 🤖 Agent configuration
└── .env.example                      # 🤖 Example environment config
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
✅ 🤖 AI agent responds to natural language queries
✅ 🤖 Agent autonomously uses tools and provides recommendations
✅ 🤖 Interactive CLI works smoothly

---

**Built with:** Python 3.7+, Pandas, NumPy, SciPy, LangChain, OpenAI/Anthropic APIs

**Author:** Audience Miner 2.0 Toy Project

**Version:** 1.0.0
