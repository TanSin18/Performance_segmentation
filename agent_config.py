"""
Agent configuration management.

Loads configuration from environment variables with sensible defaults.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class AgentConfig:
    """Configuration for the AI agent."""

    # LLM Provider Settings
    PROVIDER = os.getenv('AGENT_PROVIDER', 'openai')
    MODEL = os.getenv('AGENT_MODEL', 'gpt-4o-mini')
    VERBOSE = os.getenv('AGENT_VERBOSE', 'true').lower() == 'true'

    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Campaign Analysis Defaults
    DEFAULT_MAX_SEGMENTS = int(os.getenv('DEFAULT_MAX_SEGMENTS', '10'))
    DEFAULT_MIN_LIFT = float(os.getenv('DEFAULT_MIN_LIFT', '0.20'))
    DEFAULT_MIN_SEGMENT_PCT = float(os.getenv('DEFAULT_MIN_SEGMENT_PCT', '0.05'))

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'provider': cls.PROVIDER,
            'model': cls.MODEL,
            'verbose': cls.VERBOSE,
            'has_openai_key': bool(cls.OPENAI_API_KEY),
            'has_anthropic_key': bool(cls.ANTHROPIC_API_KEY),
            'default_max_segments': cls.DEFAULT_MAX_SEGMENTS,
            'default_min_lift': cls.DEFAULT_MIN_LIFT,
            'default_min_segment_pct': cls.DEFAULT_MIN_SEGMENT_PCT
        }

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """
        Validate configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if cls.PROVIDER == 'openai' and not cls.OPENAI_API_KEY:
            return False, "OPENAI_API_KEY not set. Set it in .env or environment."

        if cls.PROVIDER == 'anthropic' and not cls.ANTHROPIC_API_KEY:
            return False, "ANTHROPIC_API_KEY not set. Set it in .env or environment."

        if cls.PROVIDER not in ['openai', 'anthropic', 'ollama']:
            return False, f"Invalid provider: {cls.PROVIDER}. Must be openai, anthropic, or ollama."

        return True, ""

    @classmethod
    def print_config(cls):
        """Print current configuration."""
        config = cls.to_dict()
        print("\n📋 Agent Configuration:")
        print(f"   Provider: {config['provider']}")
        print(f"   Model: {config['model']}")
        print(f"   Verbose: {config['verbose']}")
        print(f"   OpenAI Key: {'✅ Set' if config['has_openai_key'] else '❌ Not set'}")
        print(f"   Anthropic Key: {'✅ Set' if config['has_anthropic_key'] else '❌ Not set'}")
        print(f"\n   Default Max Segments: {config['default_max_segments']}")
        print(f"   Default Min Lift: {config['default_min_lift']:.0%}")
        print(f"   Default Min Segment %: {config['default_min_segment_pct']:.0%}")
        print()


if __name__ == "__main__":
    """Test configuration loading."""
    print("🔧 Testing Agent Configuration\n")
    print("="*60)

    AgentConfig.print_config()

    is_valid, error = AgentConfig.validate()
    if is_valid:
        print("✅ Configuration is valid!")
    else:
        print(f"❌ Configuration error: {error}")
        print("\nTo fix:")
        print("1. Copy .env.example to .env")
        print("2. Add your API key(s)")
        print("3. Run this script again")
