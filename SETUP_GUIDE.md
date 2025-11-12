# Complete Setup Guide - Audience Miner 2.0

**A Beginner-Friendly, Step-by-Step Guide**

This guide will walk you through EVERYTHING you need to use this repository, from installing Python to running your first AI agent analysis. No prior knowledge assumed!

---

## Table of Contents

1. [Prerequisites - What You Need](#1-prerequisites---what-you-need)
2. [Installation - Step by Step](#2-installation---step-by-step)
3. [Configuration - Setting Up API Keys](#3-configuration---setting-up-api-keys)
4. [Quick Start - Your First Run](#4-quick-start---your-first-run)
5. [Understanding the Files](#5-understanding-the-files)
6. [How to Use the System](#6-how-to-use-the-system)
7. [Common Workflows](#7-common-workflows)
8. [Understanding the Output](#8-understanding-the-output)
9. [Troubleshooting](#9-troubleshooting)
10. [Next Steps](#10-next-steps)

---

## 1. Prerequisites - What You Need

### A. Python Installation

**Check if Python is installed:**
```bash
python --version
# OR
python3 --version
```

**Expected output:** `Python 3.7.0` or higher

**If Python is NOT installed:**

- **Windows:** Download from [python.org](https://www.python.org/downloads/)
  - ✅ Check "Add Python to PATH" during installation
- **Mac:**
  ```bash
  brew install python3
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

### B. Git (Optional but Recommended)

**Check if Git is installed:**
```bash
git --version
```

**If NOT installed:**
- **Windows:** Download from [git-scm.com](https://git-scm.com/)
- **Mac:** `brew install git`
- **Linux:** `sudo apt install git`

### C. Text Editor (Choose ONE)

- **VS Code** (Recommended): [code.visualstudio.com](https://code.visualstudio.com/)
- **Sublime Text**: [sublimetext.com](https://www.sublimetext.com/)
- **Any text editor** (Notepad++, Atom, etc.)

### D. Terminal/Command Line

- **Windows:** Use Command Prompt, PowerShell, or Git Bash
- **Mac:** Use Terminal (Applications → Utilities → Terminal)
- **Linux:** Use your default terminal

---

## 2. Installation - Step by Step

### Step 1: Get the Code

**Option A: Download ZIP (Easy)**
1. Click the green "Code" button on GitHub
2. Click "Download ZIP"
3. Extract the ZIP file to a folder (e.g., `C:\Projects\Performance_segmentation` or `~/Projects/Performance_segmentation`)

**Option B: Clone with Git (Recommended)**
```bash
cd /path/to/where/you/want/the/project
git clone <repository-url>
cd Performance_segmentation
```

### Step 2: Open Terminal in Project Folder

Navigate to the project folder:

```bash
# Example for Mac/Linux:
cd ~/Projects/Performance_segmentation

# Example for Windows:
cd C:\Projects\Performance_segmentation
```

**Verify you're in the right place:**
```bash
ls
# You should see files like: README.md, main.py, agent_cli.py, etc.
```

### Step 3: Install Python Dependencies

**Install all required packages:**
```bash
pip install -r requirements.txt
```

**If you see "pip: command not found", try:**
```bash
pip3 install -r requirements.txt
# OR
python -m pip install -r requirements.txt
# OR
python3 -m pip install -r requirements.txt
```

**What gets installed:**
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scipy` - Statistical functions
- `langchain` - AI agent framework
- `openai` - OpenAI API client
- `anthropic` - Anthropic API client
- `python-dotenv` - Environment variable management

**Installation should take:** 1-3 minutes

---

## 3. Configuration - Setting Up API Keys

### Option 1: Use the AI Agent (Requires API Key)

To use the **AI agent** (the coolest feature!), you need an API key from OpenAI or Anthropic.

#### Step 1: Get an API Key

**For OpenAI (Recommended for Beginners):**
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. **IMPORTANT:** Copy the key immediately (you can't see it again!)
6. **Cost:** ~$0.01-0.05 per query with `gpt-4o-mini`

**For Anthropic Claude:**
1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Create an API key
4. Copy the key
5. **Cost:** ~$0.05-0.20 per query with `claude-3-5-sonnet`

#### Step 2: Create Your `.env` File

**Using Command Line:**
```bash
cp .env.example .env
```

**Using File Explorer:**
1. Find the file named `.env.example`
2. Copy it
3. Rename the copy to `.env` (just `.env`, no `.txt` or anything else)

**Windows Note:** To see/edit `.env` files, you may need to:
- Enable "Show hidden files" in File Explorer
- Use a text editor like VS Code or Notepad++

#### Step 3: Add Your API Key

Open `.env` in a text editor and add your key:

**For OpenAI:**
```bash
OPENAI_API_KEY=sk-proj-abc123...your_actual_key_here
```

**For Anthropic:**
```bash
ANTHROPIC_API_KEY=sk-ant-abc123...your_actual_key_here
```

**For Databricks (Advanced):**
```bash
DATABRICKS_TOKEN=your_databricks_token_here
```

**IMPORTANT:**
- Replace `your_openai_api_key_here` with your ACTUAL key
- No spaces around the `=` sign
- No quotes needed
- Keep this file SECRET (never commit to Git)

#### Step 4: Configure Agent Settings (Optional)

You can customize the agent behavior in `.env`:

```bash
# Which AI provider to use
AGENT_PROVIDER=openai  # Options: openai, anthropic, ollama, databricks

# Which model to use
AGENT_MODEL=gpt-4o-mini  # Options: gpt-4o-mini, gpt-4, claude-3-5-sonnet-20241022

# Show agent's thinking process
AGENT_VERBOSE=true  # Options: true, false

# Analysis settings
DEFAULT_MAX_SEGMENTS=10      # How many segments to find
DEFAULT_MIN_LIFT=0.20        # Minimum 20% performance lift
DEFAULT_MIN_SEGMENT_PCT=0.05 # Segments must be at least 5% of data
```

#### Step 5: Verify Configuration

**Test your setup:**
```bash
python agent_config.py
```

**Expected output:**
```
🔧 Testing Agent Configuration
============================================================

📋 Agent Configuration:
   Provider: openai
   Model: gpt-4o-mini
   Verbose: true
   OpenAI Key: ✅ Set
   Anthropic Key: ❌ Not set
   Databricks Token: ❌ Not set

   Default Max Segments: 10
   Default Min Lift: 20%
   Default Min Segment %: 5%

✅ Configuration is valid!
```

### Option 2: Use Without AI Agent (No API Key Needed)

You can still use the core segmentation engine without an API key!

**What you CAN do:**
- Generate synthetic campaign data
- Run statistical segmentation analysis
- Compare campaigns
- Get bid recommendations
- All the math and statistics work!

**What you CAN'T do:**
- Use natural language queries
- Interactive AI agent conversations

**Just skip to Step 4** below and use `main.py` instead of `agent_cli.py`.

---

## 4. Quick Start - Your First Run

### Option A: Run the AI Agent (Interactive Mode)

**Start the interactive agent:**
```bash
python agent_cli.py
```

**You'll see:**
```
🤖 Audience Miner AI Agent
============================================================
Type 'help' for available commands or ask anything!
Type 'exit' to quit.

You:
```

**Try these example queries:**
```
You: demo
You: analyze Campaign_A
You: show me the top 3 segments
You: compare Campaign_A and Campaign_B
You: what's the best opportunity?
```

**Exit when done:**
```
You: exit
```

### Option B: Run a Single Query

**Ask one question and get an answer:**
```bash
python agent_cli.py --query "Analyze Campaign_A and show top segments"
```

### Option C: Run Demo Mode

**See pre-programmed examples:**
```bash
python agent_cli.py --demo
```

### Option D: Run Without AI Agent

**Generate data and run analysis:**
```bash
python main.py
```

**This will:**
1. Generate synthetic data for 2 campaigns (30 seconds)
2. Run segmentation on Campaign A
3. Compare Campaign A vs Campaign B
4. Save 4 CSV files with results

**Output files created:**
- `campaign_a_data.csv` - Raw session data for Campaign A
- `campaign_b_data.csv` - Raw session data for Campaign B
- `segmentation_results.csv` - High-performing segments with bid recommendations
- `comparison_results.csv` - Campaign comparison insights

---

## 5. Understanding the Files

Here's what each file does:

### 🎯 Files You'll Use Most

| File | Purpose | When to Use |
|------|---------|-------------|
| `agent_cli.py` | **Interactive AI agent** | Main way to interact with the system |
| `main.py` | **Traditional analysis pipeline** | Run without AI agent |
| `.env` | **Your API keys and settings** | Configure before first run |
| `requirements.txt` | **Python dependencies** | Install with `pip install -r requirements.txt` |

### 🔧 Core Engine Files (You Don't Need to Edit These)

| File | Purpose |
|------|---------|
| `react_agent.py` | AI agent brain (ReAct architecture) |
| `agent_tools.py` | Tools the AI agent can use |
| `agent_config.py` | Configuration loader |
| `simple_segmentation_engine.py` | Statistical segmentation algorithm |
| `simple_comparison_engine.py` | Campaign comparison logic |
| `pandas_data_loader.py` | Data loading and aggregation |
| `mock_data_generator.py` | Synthetic data generation |

### 📚 Other Files

| File | Purpose |
|------|---------|
| `minimal_audience_miner.py` | Simplified 200-line demo |
| `test_agent_tools.py` | Unit tests |
| `README.md` | Full documentation |
| `SETUP_GUIDE.md` | This file! |

### 📁 Output Files (Created When You Run)

| File | Content |
|------|---------|
| `campaign_a_data.csv` | Raw session-level data for Campaign A |
| `campaign_b_data.csv` | Raw session-level data for Campaign B |
| `segmentation_results.csv` | Top segments with bid recommendations |
| `comparison_results.csv` | Competitive analysis |

---

## 6. How to Use the System

### Basic Workflow

```
1. Generate or load campaign data
   ↓
2. Run segmentation analysis
   ↓
3. Review top-performing segments
   ↓
4. Get bid adjustment recommendations
   ↓
5. (Optional) Compare with other campaigns
   ↓
6. Export results or take action
```

### Three Ways to Use the System

#### Method 1: AI Agent (Interactive) ⭐ RECOMMENDED

**Best for:** Exploring data, asking questions, getting explanations

```bash
python agent_cli.py
```

**Example session:**
```
You: Load Campaign_A
🤖: Loaded Campaign_A with 15,000 sessions, 375 conversions (2.5% eCR)

You: What are the best segments?
🤖: Analyzing... Found 8 high-performing segments. Top 3:
    1. income_bucket = '100K+' → +64.8% lift, 1.42x bid multiplier
    2. age_range = '35-44' → +54.2% lift, 1.38x bid multiplier
    3. education_level = 'Graduate' → +46.3% lift, 1.34x bid multiplier

You: Tell me more about the first one
🤖: The 100K+ income segment has 1,800 sessions with 74 conversions...
    [detailed explanation]

You: What's the ROI impact?
🤖: If you increase bids by 42% for this segment...
    [calculates projected revenue increase]
```

**Quick commands:**
- `analyze <campaign>` - Analyze a campaign
- `compare <camp_a> <camp_b>` - Compare two campaigns
- `segments <campaign>` - Show top segments
- `list` - List loaded campaigns
- `help` - Show help
- `exit` - Quit

#### Method 2: AI Agent (Single Query)

**Best for:** One-off questions, scripting, automation

```bash
# Ask a question
python agent_cli.py --query "Analyze Campaign_A"

# Get quick insights
python agent_cli.py -q "Show top 5 segments for Campaign_A"

# Compare campaigns
python agent_cli.py -q "Compare Campaign_A and Campaign_B"
```

#### Method 3: Traditional Pipeline (No AI)

**Best for:** Batch processing, no API key, custom workflows

```bash
python main.py
```

**What it does:**
1. Generates 2 campaigns with 15,000 sessions each
2. Runs segmentation on Campaign A
3. Compares Campaign A vs Campaign B
4. Saves 4 CSV files

**To customize, edit `main.py`:**
```python
# Change number of sessions
data_a = generate_campaign_data('Campaign_A', num_sessions=50000)

# Change attributes to analyze
attributes = ['age_range', 'income_bucket', 'device_type', 'education_level']

# Change thresholds
engine = SimpleSegmentationEngine(
    data=aggregated,
    attributes=attributes,
    max_segments=20,        # Find up to 20 segments
    min_lift=0.15,         # 15% minimum lift
    min_segment_pct=0.03   # 3% minimum size
)
```

---

## 7. Common Workflows

### Workflow 1: Analyze a Campaign

**Goal:** Find high-performing audience segments

**With AI Agent:**
```bash
python agent_cli.py
```
```
You: analyze Campaign_A
You: show me segments with at least 50% lift
You: calculate ROI for the top segment
```

**Without AI Agent:**
```python
# Edit main.py or create your own script:
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

# Print results
for i, seg in enumerate(segments[:5], 1):
    print(f"\n{i}. {seg['condition']}")
    print(f"   eCR: {seg['ecr']:.2%} (lift: {seg['ecr_lift']:+.1%})")
    print(f"   Bid Multiplier: {seg['bid_multiplier']:.2f}x")
    print(f"   Sessions: {seg['sessions']:,}")
```

### Workflow 2: Compare Two Campaigns

**Goal:** Find competitive advantages

**With AI Agent:**
```bash
python agent_cli.py
```
```
You: compare Campaign_A and Campaign_B
You: which segments does Campaign_A win in?
You: what should I optimize in Campaign_B?
```

**Without AI Agent:**
```python
# See comparison in main.py or:
from simple_comparison_engine import SimpleComparisonEngine

engine = SimpleComparisonEngine(
    data_a=aggregated_campaign_a,
    data_b=aggregated_campaign_b,
    campaign_a_id='Campaign_A',
    campaign_b_id='Campaign_B',
    attributes=['age_range', 'income_bucket'],
    min_advantage=0.20
)
comparisons = engine.compare()

for comp in comparisons[:5]:
    print(f"{comp['segment_condition']}")
    print(f"  {comp['overall_advantage']}")
    print(f"  A eCR: {comp['campaign_a_ecr']:.2%}")
    print(f"  B eCR: {comp['campaign_b_ecr']:.2%}")
    print(f"  Difference: {comp['ecr_diff_pct']:+.1%}")
```

### Workflow 3: Get Bid Recommendations

**Goal:** Get actionable bid adjustment suggestions

**With AI Agent:**
```
You: what bids should I adjust for Campaign_A?
You: give me 5 actionable recommendations
You: explain the top recommendation in detail
```

**Reading the output:**
- **Bid Multiplier < 1.0** → Decrease bids (e.g., 0.80x = -20%)
- **Bid Multiplier = 1.0** → Keep bids the same
- **Bid Multiplier > 1.0** → Increase bids (e.g., 1.40x = +40%)

**Example recommendation:**
```
INCREASE BIDS for income_bucket = '100K+'
Current eCR: 4.11% (baseline lift: +64.8%)
Recommended bid adjustment: +42% (multiplier: 1.42x)
Segment size: 1,800 sessions
Confidence: 95%

Action: Increase bids by 42% for users with income > $100K
Expected impact: +25-35% campaign ROI
```

### Workflow 4: Export and Visualize Results

**Export to CSV:**
```bash
python main.py
# Creates: segmentation_results.csv, comparison_results.csv
```

**Open in Excel/Google Sheets:**
1. Open the CSV file
2. Sort by `ecr_lift` (descending) to see best segments
3. Filter by `confidence_score > 0.90` for high confidence
4. Create charts/pivot tables

**Programmatic export:**
```python
import pandas as pd

segments_df = pd.DataFrame(segments)
segments_df.to_csv('my_analysis.csv', index=False)
segments_df.to_excel('my_analysis.xlsx', index=False)
segments_df.to_json('my_analysis.json', orient='records', indent=2)
```

---

## 8. Understanding the Output

### Segmentation Results

**Columns explained:**

| Column | What It Means | Example | Good/Bad |
|--------|---------------|---------|----------|
| `condition` | Segment definition | `income_bucket = '100K+'` | - |
| `sessions` | Number of sessions | `1,800` | Bigger = more reliable |
| `conversions` | Number of conversions | `74` | - |
| `ecr` | Conversion rate | `0.0411` (4.11%) | Higher is better |
| `ecr_lift` | Performance vs baseline | `0.648` (+64.8%) | Higher is better |
| `bid_multiplier` | Recommended bid change | `1.42` (+42% bids) | >1.0 = increase, <1.0 = decrease |
| `confidence_score` | How confident (0-1) | `0.95` (95%) | >0.90 is excellent |
| `feature_importance` | Cramér's V | `0.45` | >0.20 is good |

**Example row:**
```
condition: income_bucket = '100K+'
sessions: 1,800
conversions: 74
ecr: 0.0411 (4.11%)
ecr_lift: 0.648 (+64.8%)
bid_multiplier: 1.42
confidence_score: 0.95
feature_importance: 0.45
```

**Translation:**
- Users with income >$100K convert at 4.11%
- This is 64.8% better than average
- Increase bids by 42% for this segment
- We're 95% confident this is real
- Income is a very important factor (Cramér's V = 0.45)

### Comparison Results

**Columns explained:**

| Column | What It Means | Example |
|--------|---------------|---------|
| `segment_condition` | Segment | `income_bucket = '100K+'` |
| `overall_advantage` | Which campaign wins | `Strong Campaign_A Advantage` |
| `campaign_a_ecr` | Campaign A conversion rate | `0.0411` (4.11%) |
| `campaign_b_ecr` | Campaign B conversion rate | `0.0301` (3.01%) |
| `ecr_diff_pct` | Performance difference | `0.369` (+36.9% for A) |

**Translation:**
- Campaign A performs 36.9% better than Campaign B for high-income users
- This is a "Strong" advantage (>30% difference)
- Consider applying Campaign A's tactics to Campaign B

---

## 9. Troubleshooting

### Problem: "pip: command not found"

**Solution:** Try these alternatives:
```bash
pip3 install -r requirements.txt
python -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```

### Problem: "OPENAI_API_KEY not set"

**Symptoms:**
```
❌ Configuration error: OPENAI_API_KEY not set
```

**Solution:**
1. Check `.env` file exists (not `.env.example`)
2. Open `.env` in text editor
3. Make sure line looks like: `OPENAI_API_KEY=sk-proj-abc123...`
4. No spaces around `=`
5. No quotes around the key
6. Save the file
7. Try again

**Still not working?**
```bash
# Set in terminal (temporary):
export OPENAI_API_KEY='your-key-here'
python agent_cli.py
```

### Problem: "Rate limit exceeded"

**Symptoms:**
```
Error: Rate limit exceeded
```

**Solution:**
- Wait 60 seconds and try again
- Use a cheaper model: `--model gpt-4o-mini`
- Upgrade your API plan at OpenAI

### Problem: "No segments found"

**Symptoms:**
```
Found 0 segments
```

**Solutions:**
1. **Lower the lift threshold:**
   ```python
   engine = SimpleSegmentationEngine(
       data=aggregated,
       attributes=attributes,
       min_lift=0.10  # Lower from 0.20 to 0.10
   )
   ```

2. **Lower the minimum segment size:**
   ```python
   min_segment_pct=0.02  # Lower from 0.05 to 0.02
   ```

3. **Generate more data:**
   ```python
   data = generate_campaign_data('Campaign_A', num_sessions=50000)
   ```

### Problem: "ModuleNotFoundError: No module named 'X'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```bash
pip install -r requirements.txt
```

If that doesn't work:
```bash
pip install pandas numpy scipy langchain langchain-openai anthropic python-dotenv
```

### Problem: "Agent gives poor quality answers"

**Solutions:**
1. **Use a better model:**
   ```bash
   python agent_cli.py --model gpt-4
   ```

2. **Enable verbose mode to see thinking:**
   ```bash
   python agent_cli.py --verbose
   ```

3. **Be more specific in your query:**
   - ❌ "analyze this"
   - ✅ "analyze Campaign_A and show me segments with at least 50% lift in conversion rate"

### Problem: "Permission denied" (Mac/Linux)

**Symptoms:**
```
bash: ./agent_cli.py: Permission denied
```

**Solution:**
```bash
# Make file executable:
chmod +x agent_cli.py

# Or run with python:
python agent_cli.py
```

### Problem: "SyntaxError" or "Invalid syntax"

**Cause:** Using Python 2 instead of Python 3

**Solution:**
```bash
# Check version:
python --version

# Use python3:
python3 agent_cli.py
```

---

## 10. Next Steps

### Learn More

1. **Read the full README.md** for technical details
2. **Explore the code:**
   - Start with `simple_segmentation_engine.py` (core algorithm)
   - Check `agent_tools.py` (what the AI can do)
   - Read `mock_data_generator.py` (how data is created)

3. **Customize the analysis:**
   - Edit `main.py` to change settings
   - Add new attributes in `mock_data_generator.py`
   - Adjust thresholds for your use case

### Advanced Usage

**Run with local LLM (no API key needed):**
```bash
# Install Ollama: https://ollama.ai
ollama pull llama3
python agent_cli.py --provider ollama --model llama3
```

**Use different models:**
```bash
# OpenAI GPT-4 (better quality, more expensive)
python agent_cli.py --model gpt-4

# Anthropic Claude Sonnet
python agent_cli.py --provider anthropic --model claude-3-5-sonnet-20241022

# Databricks (if you have access)
python agent_cli.py --provider databricks --model databricks-gpt-5
```

**Create your own analysis script:**
```python
from react_agent import create_agent

agent = create_agent(provider='openai', model='gpt-4o-mini')
response = agent.chat("Analyze Campaign_A and show top segments")
print(response)
```

**Run tests:**
```bash
python test_agent_tools.py
```

**Run minimal demo:**
```bash
python minimal_audience_miner.py
```

### Get Help

**Documentation:**
- `README.md` - Full documentation
- Code comments - Every function has docstrings
- `.env.example` - Configuration examples

**Check configuration:**
```bash
python agent_config.py
```

**Test installation:**
```bash
python -c "import pandas, numpy, scipy, langchain; print('All imports successful!')"
```

---

## Quick Reference Card

**Start interactive agent:**
```bash
python agent_cli.py
```

**Run traditional analysis:**
```bash
python main.py
```

**Single query:**
```bash
python agent_cli.py -q "your question here"
```

**Demo mode:**
```bash
python agent_cli.py --demo
```

**Check configuration:**
```bash
python agent_config.py
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Output files:**
- `segmentation_results.csv` - Top segments
- `comparison_results.csv` - Campaign comparison
- `campaign_a_data.csv` - Raw data A
- `campaign_b_data.csv` - Raw data B

---

## Success Checklist

✅ **Installation Complete:**
- [ ] Python 3.7+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] No errors when running `python agent_config.py`

✅ **Configuration Complete (if using AI agent):**
- [ ] `.env` file created (copied from `.env.example`)
- [ ] API key added to `.env`
- [ ] `python agent_config.py` shows "✅ Configuration is valid!"

✅ **First Run Successful:**
- [ ] `python main.py` runs without errors
- [ ] 4 CSV files created
- [ ] OR `python agent_cli.py` starts successfully

✅ **Understanding:**
- [ ] I know which files do what
- [ ] I can run segmentation analysis
- [ ] I understand the output columns
- [ ] I can interpret bid multipliers

---

**Congratulations! You're ready to use Audience Miner 2.0!** 🎉

If you get stuck, refer to the [Troubleshooting](#9-troubleshooting) section or check the code comments.
