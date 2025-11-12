#!/usr/bin/env python3
"""
Agent CLI - Interactive command-line interface for the campaign optimization agent.

Usage:
    python agent_cli.py                    # Interactive mode
    python agent_cli.py --query "..."      # Single query mode
    python agent_cli.py --demo             # Run demo queries
"""

import sys
import os
import argparse
from typing import Optional
import json

from react_agent import create_agent, CampaignOptimizationAgent


# ANSI color codes for better output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Print welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        🤖 Campaign Optimization AI Agent                          ║
║        Powered by ReAct (Reasoning + Acting)                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    print(Colors.OKBLUE + banner + Colors.ENDC)


def print_help():
    """Print help information."""
    help_text = """
📚 Available Commands:

    analyze <campaign_id>           - Analyze a campaign and get recommendations
    compare <campaign_a> <campaign_b> - Compare two campaigns
    segments <campaign_id>          - Show top performing segments
    details <campaign_id> <segment> - Get detailed segment info
    roi <campaign_id> <segment>     - Calculate ROI impact
    list                            - List loaded campaigns
    help                            - Show this help
    clear                           - Clear screen
    exit / quit                     - Exit the CLI

💡 Example Queries (natural language):

    "Analyze Campaign_A and find the best segments"
    "Which segments should I increase bids for in Campaign_B?"
    "Compare Campaign_A and Campaign_B"
    "What's the ROI impact of optimizing the income=100K+ segment?"
    "Show me segments with at least 50% lift"
    "Give me top 5 recommendations for Campaign_C"

⚙️  Configuration:

    Set API key: export OPENAI_API_KEY='your-key'
    Use Anthropic: export ANTHROPIC_API_KEY='your-key' (modify code)
    Use Ollama: Install locally and modify code to use provider='ollama'
"""
    print(help_text)


def parse_command(user_input: str) -> tuple:
    """Parse user command and arguments."""
    parts = user_input.strip().split()
    if not parts:
        return None, []

    command = parts[0].lower()
    args = parts[1:]
    return command, args


def handle_command(command: str, args: list, agent: CampaignOptimizationAgent) -> Optional[str]:
    """Handle special commands. Returns None if not a special command."""

    if command in ['exit', 'quit', 'q']:
        print(Colors.OKGREEN + "\n👋 Goodbye! Thanks for using the agent.\n" + Colors.ENDC)
        sys.exit(0)

    elif command == 'help':
        print_help()
        return ""

    elif command == 'clear':
        os.system('clear' if os.name != 'nt' else 'cls')
        print_banner()
        return ""

    elif command == 'list':
        return agent.chat("List all loaded campaigns")

    elif command == 'analyze' and len(args) >= 1:
        campaign_id = args[0]
        return agent.chat(f"Analyze {campaign_id} and provide top optimization recommendations")

    elif command == 'compare' and len(args) >= 2:
        campaign_a, campaign_b = args[0], args[1]
        return agent.chat(f"Compare {campaign_a} and {campaign_b}. Show me the competitive advantages.")

    elif command == 'segments' and len(args) >= 1:
        campaign_id = args[0]
        max_segments = args[1] if len(args) > 1 else "10"
        return agent.chat(f"Show me the top {max_segments} segments for {campaign_id}")

    elif command == 'details' and len(args) >= 2:
        campaign_id = args[0]
        segment = ' '.join(args[1:])
        return agent.chat(f"Get detailed information for segment {segment} in {campaign_id}")

    elif command == 'roi' and len(args) >= 2:
        campaign_id = args[0]
        segment = ' '.join(args[1:])
        return agent.chat(f"Calculate the ROI impact of optimizing {segment} in {campaign_id}")

    return None  # Not a special command, treat as natural language


def run_interactive_mode(agent: CampaignOptimizationAgent):
    """Run the agent in interactive mode."""
    print_banner()
    print(Colors.OKGREEN + "✅ Agent initialized successfully!\n" + Colors.ENDC)
    print("Type 'help' for commands, or just ask me anything in natural language.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            # Get user input
            user_input = input(Colors.BOLD + "You: " + Colors.ENDC).strip()

            if not user_input:
                continue

            # Parse command
            command, args = parse_command(user_input)

            # Handle special commands
            response = handle_command(command, args, agent)

            # If not a special command, treat as natural language query
            if response is None:
                print(Colors.OKCYAN + "\n🤖 Agent: " + Colors.ENDC + "Thinking...\n")
                response = agent.chat(user_input)

            # Display response
            if response:
                print(Colors.OKCYAN + "\n🤖 Agent: " + Colors.ENDC)
                print(response)
                print()

        except KeyboardInterrupt:
            print(Colors.WARNING + "\n\n⚠️  Interrupted. Type 'exit' to quit.\n" + Colors.ENDC)
        except Exception as e:
            print(Colors.FAIL + f"\n❌ Error: {str(e)}\n" + Colors.ENDC)


def run_single_query(agent: CampaignOptimizationAgent, query: str):
    """Run a single query and exit."""
    print(Colors.OKCYAN + f"\n🤖 Query: {query}\n" + Colors.ENDC)
    print(Colors.OKGREEN + "Processing...\n" + Colors.ENDC)

    response = agent.chat(query)

    print(Colors.OKCYAN + "🤖 Response:\n" + Colors.ENDC)
    print(response)
    print()


def run_demo(agent: CampaignOptimizationAgent):
    """Run demo queries."""
    print_banner()
    print(Colors.OKGREEN + "🎬 Running Demo Queries...\n" + Colors.ENDC)

    demo_queries = [
        {
            "name": "Load Campaign Data",
            "query": "Load Campaign_A data"
        },
        {
            "name": "Find Top Segments",
            "query": "What are the top 3 performing segments for Campaign_A?"
        },
        {
            "name": "Get Recommendations",
            "query": "Give me actionable bid recommendations for Campaign_A"
        },
        {
            "name": "Compare Campaigns",
            "query": "Load Campaign_B and compare it to Campaign_A. Which one is better?"
        },
        {
            "name": "ROI Analysis",
            "query": "For the best segment in Campaign_A, what's the potential ROI impact?"
        }
    ]

    for i, demo in enumerate(demo_queries, 1):
        print(f"\n{'='*70}")
        print(f"{Colors.BOLD}Demo {i}/{len(demo_queries)}: {demo['name']}{Colors.ENDC}")
        print(f"{'='*70}\n")
        print(f"{Colors.OKCYAN}Query: {demo['query']}{Colors.ENDC}\n")

        try:
            response = agent.chat(demo['query'])
            print(f"{Colors.OKGREEN}Response:{Colors.ENDC}")
            print(response)
            print()

            # Pause between queries
            if i < len(demo_queries):
                input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        except Exception as e:
            print(f"{Colors.FAIL}Error: {str(e)}{Colors.ENDC}")

    print(f"\n{Colors.OKGREEN}✅ Demo complete!{Colors.ENDC}\n")


def check_api_keys() -> tuple:
    """Check which API keys are available."""
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    return openai_key, anthropic_key


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Campaign Optimization AI Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Run a single query and exit'
    )
    parser.add_argument(
        '--demo', '-d',
        action='store_true',
        help='Run demo queries'
    )
    parser.add_argument(
        '--provider', '-p',
        type=str,
        choices=['openai', 'anthropic', 'ollama'],
        default='openai',
        help='LLM provider to use (default: openai)'
    )
    parser.add_argument(
        '--model', '-m',
        type=str,
        help='Model name (e.g., gpt-4, claude-3-5-sonnet-20241022, llama3)'
    )
    parser.add_argument(
        '--no-verbose', '-nv',
        action='store_true',
        help='Disable verbose output (hide agent reasoning)'
    )

    args = parser.parse_args()

    # Check for API keys
    openai_key, anthropic_key = check_api_keys()

    if args.provider == 'openai' and not openai_key:
        print(f"{Colors.FAIL}❌ Error: OPENAI_API_KEY not found{Colors.ENDC}")
        print("\nSet your API key:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("\nOr use a different provider:")
        print("  --provider anthropic (requires ANTHROPIC_API_KEY)")
        print("  --provider ollama (requires local Ollama installation)")
        sys.exit(1)

    if args.provider == 'anthropic' and not anthropic_key:
        print(f"{Colors.FAIL}❌ Error: ANTHROPIC_API_KEY not found{Colors.ENDC}")
        print("\nSet your API key:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    # Determine model
    model = args.model
    if not model:
        if args.provider == 'openai':
            model = 'gpt-4o-mini'  # Cheaper, faster
        elif args.provider == 'anthropic':
            model = 'claude-3-5-sonnet-20241022'
        elif args.provider == 'ollama':
            model = 'llama3'

    # Initialize agent
    try:
        print(f"\n{Colors.OKBLUE}🔧 Initializing agent...{Colors.ENDC}")
        print(f"   Provider: {args.provider}")
        print(f"   Model: {model}")
        print()

        agent = create_agent(
            provider=args.provider,
            model=model,
            verbose=not args.no_verbose
        )

    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to initialize agent: {str(e)}{Colors.ENDC}")
        sys.exit(1)

    # Run appropriate mode
    if args.demo:
        run_demo(agent)
    elif args.query:
        run_single_query(agent, args.query)
    else:
        run_interactive_mode(agent)


if __name__ == "__main__":
    main()
