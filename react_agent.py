"""
ReAct Agent - Reasoning and Acting agent for campaign optimization.

This module implements an AI agent that can reason about campaigns,
use tools to analyze data, and provide actionable recommendations.
"""

import os
from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama

from agent_tools import get_tools_instance


# Agent system prompt
REACT_PROMPT_TEMPLATE = """You are an expert AI agent for digital advertising campaign optimization. You help analyze audience segments, identify high-performing groups, and recommend bid adjustments to maximize ROI.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question or task you must address
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT GUIDELINES:
1. Always load campaign data before analyzing it
2. Use run_segmentation_analysis to find top performing segments
3. Provide clear, actionable recommendations with specific bid adjustments
4. Explain your reasoning and the statistical significance of findings
5. When comparing campaigns, highlight competitive advantages
6. Be concise but thorough in your analysis
7. If you don't have enough information, use tools to gather it
8. Always validate segments are statistically significant before recommending changes

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""


class CampaignOptimizationAgent:
    """
    ReAct agent for campaign optimization and analysis.
    """

    def __init__(
        self,
        model_provider: str = "openai",
        model_name: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        verbose: bool = True
    ):
        """
        Initialize the ReAct agent.

        Args:
            model_provider: LLM provider ("openai", "anthropic", "ollama")
            model_name: Name of the model to use
            api_key: API key for the provider (if required)
            temperature: LLM temperature (0 = deterministic)
            verbose: Whether to show agent reasoning steps
        """
        self.model_provider = model_provider
        self.model_name = model_name
        self.verbose = verbose

        # Initialize tools
        self.tools_instance = get_tools_instance()
        self.tools = self._create_tools()

        # Initialize LLM
        self.llm = self._initialize_llm(api_key, temperature)

        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Create agent
        self.agent = self._create_agent()

    def _initialize_llm(self, api_key: Optional[str], temperature: float):
        """Initialize the LLM based on provider."""
        if self.model_provider == "openai":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
            return ChatOpenAI(
                model=self.model_name,
                temperature=temperature,
                api_key=api_key
            )
        elif self.model_provider == "anthropic":
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable.")
            return ChatAnthropic(
                model=self.model_name,
                temperature=temperature,
                api_key=api_key
            )
        elif self.model_provider == "ollama":
            # Ollama runs locally, no API key needed
            return Ollama(
                model=self.model_name,
                temperature=temperature
            )
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")

    def _create_tools(self) -> List[Tool]:
        """Create LangChain tools from the campaign analysis functions."""
        return [
            Tool(
                name="load_campaign_data",
                func=self.tools_instance.load_campaign_data,
                description=(
                    "Load campaign data and get summary statistics. "
                    "Input: campaign_id (string). "
                    "Returns: JSON with total sessions, conversions, revenue, eCR, RPS. "
                    "Use this FIRST before any analysis."
                )
            ),
            Tool(
                name="run_segmentation_analysis",
                func=self.tools_instance.run_segmentation_analysis,
                description=(
                    "Analyze campaign to find high-performing audience segments. "
                    "Input: campaign_id (string), optionally max_segments (int), min_lift (float). "
                    "Returns: JSON with top segments ranked by performance lift. "
                    "Each segment includes eCR, lift, bid multiplier, and confidence scores."
                )
            ),
            Tool(
                name="compare_campaigns",
                func=self.tools_instance.compare_campaigns,
                description=(
                    "Compare two campaigns to identify competitive advantages. "
                    "Input: campaign_a_id (string), campaign_b_id (string), optionally min_advantage (float). "
                    "Returns: JSON showing which campaign performs better in each segment."
                )
            ),
            Tool(
                name="get_segment_details",
                func=self.tools_instance.get_segment_details,
                description=(
                    "Get detailed metrics for a specific segment. "
                    "Input: campaign_id (string), segment_condition (string like \"income_bucket = '100K+'\"). "
                    "Returns: JSON with detailed performance metrics, statistical validation, and recommendations."
                )
            ),
            Tool(
                name="calculate_roi_impact",
                func=self.tools_instance.calculate_roi_impact,
                description=(
                    "Calculate potential ROI impact of optimizing a segment. "
                    "Input: campaign_id (string), segment_condition (string), optionally current_cpc (float), budget_allocation_pct (float). "
                    "Returns: JSON with current vs projected ROI, revenue, and cost analysis."
                )
            ),
            Tool(
                name="list_campaigns",
                func=self.tools_instance.list_available_campaigns,
                description=(
                    "List all campaigns currently loaded in memory. "
                    "Input: none. "
                    "Returns: JSON with list of available campaign IDs."
                )
            ),
            Tool(
                name="get_recommendations",
                func=self.tools_instance.get_recommendations_summary,
                description=(
                    "Get actionable optimization recommendations for a campaign. "
                    "Input: campaign_id (string), optionally top_n (int). "
                    "Returns: Human-readable summary of top recommendations with bid adjustments."
                )
            )
        ]

    def _create_agent(self) -> AgentExecutor:
        """Create the ReAct agent with tools and prompt."""
        prompt = PromptTemplate(
            template=REACT_PROMPT_TEMPLATE,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )

        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            max_iterations=10,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )

    def run(self, query: str) -> Dict[str, Any]:
        """
        Run the agent with a query.

        Args:
            query: User's question or task

        Returns:
            Dict with 'output' (final answer) and 'intermediate_steps' (reasoning)
        """
        try:
            result = self.agent.invoke({"input": query})
            return result
        except Exception as e:
            return {
                "output": f"Error: {str(e)}",
                "intermediate_steps": []
            }

    def chat(self, message: str) -> str:
        """
        Chat interface for the agent.

        Args:
            message: User message

        Returns:
            Agent's response
        """
        result = self.run(message)
        return result.get("output", "No response generated")


def create_agent(
    provider: str = "openai",
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    verbose: bool = True
) -> CampaignOptimizationAgent:
    """
    Factory function to create an agent instance.

    Args:
        provider: LLM provider ("openai", "anthropic", "ollama")
        model: Model name
        api_key: API key (optional, can use environment variable)
        verbose: Show reasoning steps

    Returns:
        Configured agent instance

    Examples:
        >>> # Using OpenAI
        >>> agent = create_agent(provider="openai", model="gpt-4")

        >>> # Using Anthropic Claude
        >>> agent = create_agent(provider="anthropic", model="claude-3-5-sonnet-20241022")

        >>> # Using local Ollama
        >>> agent = create_agent(provider="ollama", model="llama3")
    """
    return CampaignOptimizationAgent(
        model_provider=provider,
        model_name=model,
        api_key=api_key,
        verbose=verbose
    )


# Convenience functions for common tasks
def analyze_campaign(campaign_id: str, agent: Optional[CampaignOptimizationAgent] = None) -> str:
    """Quick analysis of a campaign."""
    if agent is None:
        agent = create_agent()

    query = f"Analyze {campaign_id} and provide optimization recommendations"
    return agent.chat(query)


def compare_two_campaigns(
    campaign_a: str,
    campaign_b: str,
    agent: Optional[CampaignOptimizationAgent] = None
) -> str:
    """Quick comparison of two campaigns."""
    if agent is None:
        agent = create_agent()

    query = f"Compare {campaign_a} and {campaign_b}. Which one performs better and where?"
    return agent.chat(query)


if __name__ == "__main__":
    """Demo usage of the ReAct agent."""
    print("🤖 Campaign Optimization ReAct Agent Demo\n")
    print("=" * 70)

    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  No API key found!")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")
        print("\nExample:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("  python react_agent.py")
        print("\nOr use local Ollama:")
        print("  Install: https://ollama.ai")
        print("  Run: ollama pull llama3")
        print("\nThen modify this script to use provider='ollama'")
        exit(1)

    try:
        # Create agent (defaults to OpenAI)
        print("\n🔧 Initializing agent...")
        agent = create_agent(verbose=True)

        # Example queries
        queries = [
            "Load Campaign_A data and show me the summary",
            "What are the top 3 performing segments for Campaign_A?",
            "Give me detailed recommendations for Campaign_A"
        ]

        for i, query in enumerate(queries, 1):
            print(f"\n{'='*70}")
            print(f"Query {i}: {query}")
            print(f"{'='*70}\n")

            response = agent.chat(query)
            print(f"\n📊 Agent Response:\n{response}\n")

        print("\n✅ Demo complete!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure API key is set correctly")
        print("2. Check internet connection")
        print("3. Verify API credits/quota")
