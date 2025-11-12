"""
Agent Tools - Wraps existing functionality as tools for the ReAct agent.

This module provides tool interfaces for the AI agent to interact with
the performance segmentation system.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from mock_data_generator import generate_campaign_data
from pandas_data_loader import PandasDataLoader
from simple_segmentation_engine import SimpleSegmentationEngine
from simple_comparison_engine import SimpleComparisonEngine


class CampaignAnalysisTools:
    """Collection of tools for campaign analysis and optimization."""

    def __init__(self):
        """Initialize tools with cache for loaded data."""
        self.data_cache = {}
        self.analysis_cache = {}

    def load_campaign_data(
        self,
        campaign_id: str,
        num_sessions: int = 15000,
        attributes: Optional[List[str]] = None
    ) -> str:
        """
        Load and aggregate campaign data.

        Args:
            campaign_id: Campaign identifier
            num_sessions: Number of sessions to generate
            attributes: List of demographic attributes to include

        Returns:
            JSON string with summary statistics
        """
        try:
            # Parse inputs if they come as strings (from LangChain)
            if isinstance(num_sessions, str):
                num_sessions = int(num_sessions)

            if attributes is None:
                attributes = ['age_range', 'income_bucket', 'education_level']

            # Generate synthetic data
            raw_data = generate_campaign_data(campaign_id, num_sessions)

            # Aggregate data
            loader = PandasDataLoader(
                data_source=raw_data,
                campaign_id=campaign_id,
                start_date='2024-01-01',
                end_date='2024-12-31',
                attributes=attributes
            )
            aggregated = loader.load_campaign_data()

            # Cache the data
            cache_key = f"{campaign_id}_{num_sessions}"
            self.data_cache[cache_key] = {
                'aggregated': aggregated,
                'attributes': attributes,
                'raw_data': raw_data
            }

            # Calculate summary stats
            total_sessions = aggregated['viewed_sessions'].sum()
            total_conversions = aggregated['conversions'].sum()
            total_revenue = aggregated['revenue'].sum()
            overall_ecr = total_conversions / total_sessions if total_sessions > 0 else 0
            overall_rps = total_revenue / total_sessions if total_sessions > 0 else 0

            summary = {
                'campaign_id': campaign_id,
                'total_sessions': int(total_sessions),
                'total_conversions': int(total_conversions),
                'total_revenue': float(total_revenue),
                'overall_ecr': float(overall_ecr),
                'overall_rps': float(overall_rps),
                'attributes': attributes,
                'num_segments': len(aggregated)
            }

            return json.dumps(summary, indent=2)

        except Exception as e:
            return f"Error loading campaign data: {str(e)}"

    def run_segmentation_analysis(
        self,
        campaign_id: str,
        max_segments: int = 10,
        min_lift: float = 0.20,
        min_segment_pct: float = 0.05
    ) -> str:
        """
        Run segmentation analysis to find high-performing audience segments.

        Args:
            campaign_id: Campaign identifier
            max_segments: Maximum number of segments to return
            min_lift: Minimum eCR lift threshold (default 20%)
            min_segment_pct: Minimum segment size as % of total

        Returns:
            JSON string with top performing segments
        """
        try:
            # Parse inputs if they come as strings
            if isinstance(max_segments, str):
                max_segments = int(max_segments)
            if isinstance(min_lift, str):
                min_lift = float(min_lift)
            if isinstance(min_segment_pct, str):
                min_segment_pct = float(min_segment_pct)
            # Get cached data
            cache_key = f"{campaign_id}_15000"  # Default size
            if cache_key not in self.data_cache:
                # Load data first
                self.load_campaign_data(campaign_id)

            cached = self.data_cache[cache_key]
            aggregated = cached['aggregated']
            attributes = cached['attributes']

            # Run segmentation
            engine = SimpleSegmentationEngine(
                data=aggregated,
                attributes=attributes,
                max_segments=max_segments,
                min_lift=min_lift,
                min_segment_pct=min_segment_pct
            )
            segments = engine.find_segments()

            # Cache results
            self.analysis_cache[f"{campaign_id}_segments"] = segments

            if not segments:
                return "No significant segments found. Try lowering min_lift or min_segment_pct."

            # Format top segments for readability
            top_segments = segments[:5]  # Top 5 for summary
            results = {
                'campaign_id': campaign_id,
                'total_segments_found': len(segments),
                'top_segments': [
                    {
                        'rank': i + 1,
                        'condition': seg['condition'],
                        'sessions': int(seg['sessions']),
                        'ecr': f"{seg['ecr']:.2%}",
                        'ecr_lift': f"{seg['ecr_lift']:+.1%}",
                        'bid_multiplier': f"{seg['bid_multiplier']:.2f}x",
                        'feature_importance': f"{seg['feature_importance']:.3f}",
                        'confidence': f"{seg['confidence_score']:.2%}"
                    }
                    for i, seg in enumerate(top_segments)
                ]
            }

            return json.dumps(results, indent=2)

        except Exception as e:
            return f"Error running segmentation: {str(e)}"

    def compare_campaigns(
        self,
        campaign_a_id: str,
        campaign_b_id: str,
        min_advantage: float = 0.20
    ) -> str:
        """
        Compare two campaigns to find competitive advantages.

        Args:
            campaign_a_id: First campaign identifier
            campaign_b_id: Second campaign identifier
            min_advantage: Minimum performance difference to report

        Returns:
            JSON string with comparison insights
        """
        try:
            # Parse inputs
            if isinstance(min_advantage, str):
                min_advantage = float(min_advantage)
            # Load both campaigns
            cache_key_a = f"{campaign_a_id}_15000"
            cache_key_b = f"{campaign_b_id}_15000"

            if cache_key_a not in self.data_cache:
                self.load_campaign_data(campaign_a_id)
            if cache_key_b not in self.data_cache:
                self.load_campaign_data(campaign_b_id)

            cached_a = self.data_cache[cache_key_a]
            cached_b = self.data_cache[cache_key_b]

            # Run comparison
            engine = SimpleComparisonEngine(
                data_a=cached_a['aggregated'],
                data_b=cached_b['aggregated'],
                campaign_a_id=campaign_a_id,
                campaign_b_id=campaign_b_id,
                attributes=cached_a['attributes'],
                min_advantage=min_advantage
            )
            comparisons = engine.compare()

            if not comparisons:
                return f"No significant differences found between campaigns (min_advantage={min_advantage})."

            # Format top comparisons
            top_comparisons = comparisons[:5]
            results = {
                'campaign_a': campaign_a_id,
                'campaign_b': campaign_b_id,
                'total_differences_found': len(comparisons),
                'top_insights': [
                    {
                        'segment': comp['segment_condition'],
                        'advantage': comp['overall_advantage'],
                        f'{campaign_a_id}_ecr': f"{comp['campaign_a_ecr']:.2%}",
                        f'{campaign_b_id}_ecr': f"{comp['campaign_b_ecr']:.2%}",
                        'ecr_difference': f"{comp['ecr_diff_pct']:+.1%}",
                        f'{campaign_a_id}_rps': f"${comp['campaign_a_rps']:.2f}",
                        f'{campaign_b_id}_rps': f"${comp['campaign_b_rps']:.2f}"
                    }
                    for comp in top_comparisons
                ]
            }

            return json.dumps(results, indent=2)

        except Exception as e:
            return f"Error comparing campaigns: {str(e)}"

    def get_segment_details(
        self,
        campaign_id: str,
        segment_condition: str
    ) -> str:
        """
        Get detailed information about a specific segment.

        Args:
            campaign_id: Campaign identifier
            segment_condition: Segment condition (e.g., "income_bucket = '100K+'")

        Returns:
            JSON string with detailed segment metrics
        """
        try:
            # Check if we have cached segments
            cache_key = f"{campaign_id}_segments"
            if cache_key not in self.analysis_cache:
                # Run segmentation first
                self.run_segmentation_analysis(campaign_id)

            segments = self.analysis_cache[cache_key]

            # Find matching segment
            matching_segment = None
            for seg in segments:
                if seg['condition'] == segment_condition:
                    matching_segment = seg
                    break

            if not matching_segment:
                return f"Segment '{segment_condition}' not found. Available segments: {[s['condition'] for s in segments[:5]]}"

            # Format detailed info
            details = {
                'condition': matching_segment['condition'],
                'attribute': matching_segment['attribute'],
                'value': matching_segment['value'],
                'sessions': int(matching_segment['sessions']),
                'conversions': int(matching_segment['conversions']),
                'revenue': f"${matching_segment['revenue']:.2f}",
                'metrics': {
                    'ecr': f"{matching_segment['ecr']:.2%}",
                    'ecr_lift': f"{matching_segment['ecr_lift']:+.1%}",
                    'rps': f"${matching_segment['rps']:.2f}",
                    'rps_lift': f"{matching_segment['rps_lift']:+.1%}",
                    'ctr': f"{matching_segment['ctr']:.2%}",
                    'ctr_lift': f"{matching_segment['ctr_lift']:+.1%}"
                },
                'recommendations': {
                    'bid_multiplier': f"{matching_segment['bid_multiplier']:.2f}x",
                    'bid_change': f"{(matching_segment['bid_multiplier'] - 1) * 100:+.0f}%",
                    'confidence': f"{matching_segment['confidence_score']:.2%}"
                },
                'statistical_validation': {
                    'feature_importance': f"{matching_segment['feature_importance']:.3f}",
                    'chi_square_pvalue': f"{matching_segment.get('chi_square_pvalue', 0):.4f}",
                    'is_significant': matching_segment.get('chi_square_pvalue', 1) < 0.05
                }
            }

            return json.dumps(details, indent=2)

        except Exception as e:
            return f"Error getting segment details: {str(e)}"

    def calculate_roi_impact(
        self,
        campaign_id: str,
        segment_condition: str,
        current_cpc: float = 1.50,
        budget_allocation_pct: float = 100.0
    ) -> str:
        """
        Calculate potential ROI impact of optimizing a segment.

        Args:
            campaign_id: Campaign identifier
            segment_condition: Segment to optimize
            current_cpc: Current cost per click
            budget_allocation_pct: What % of budget to allocate to this segment

        Returns:
            JSON string with ROI projections
        """
        try:
            # Parse inputs
            if isinstance(current_cpc, str):
                current_cpc = float(current_cpc)
            if isinstance(budget_allocation_pct, str):
                budget_allocation_pct = float(budget_allocation_pct)
            # Get segment details
            cache_key = f"{campaign_id}_segments"
            if cache_key not in self.analysis_cache:
                self.run_segmentation_analysis(campaign_id)

            segments = self.analysis_cache[cache_key]
            matching_segment = None
            for seg in segments:
                if seg['condition'] == segment_condition:
                    matching_segment = seg
                    break

            if not matching_segment:
                return f"Segment '{segment_condition}' not found."

            # Calculate current and projected performance
            sessions = matching_segment['sessions']
            ecr = matching_segment['ecr']
            rps = matching_segment['rps']
            bid_multiplier = matching_segment['bid_multiplier']

            # Assume linear scaling for simplicity
            current_cost = sessions * current_cpc
            current_revenue = sessions * rps
            current_roi = ((current_revenue - current_cost) / current_cost * 100) if current_cost > 0 else 0

            # Projected with bid adjustment (assuming conversions scale with bid)
            projected_sessions = sessions * (budget_allocation_pct / 100)
            projected_cpc = current_cpc * bid_multiplier
            projected_cost = projected_sessions * projected_cpc
            projected_revenue = projected_sessions * rps  # Using segment's higher RPS
            projected_roi = ((projected_revenue - projected_cost) / projected_cost * 100) if projected_cost > 0 else 0

            impact = {
                'segment': segment_condition,
                'current_performance': {
                    'sessions': int(sessions),
                    'cost': f"${current_cost:.2f}",
                    'revenue': f"${current_revenue:.2f}",
                    'roi': f"{current_roi:.1f}%"
                },
                'recommended_strategy': {
                    'bid_multiplier': f"{bid_multiplier:.2f}x",
                    'new_cpc': f"${projected_cpc:.2f}",
                    'budget_allocation': f"{budget_allocation_pct:.0f}%"
                },
                'projected_performance': {
                    'sessions': int(projected_sessions),
                    'cost': f"${projected_cost:.2f}",
                    'revenue': f"${projected_revenue:.2f}",
                    'roi': f"{projected_roi:.1f}%"
                },
                'impact': {
                    'roi_change': f"{projected_roi - current_roi:+.1f} percentage points",
                    'revenue_change': f"${projected_revenue - current_revenue:+.2f}",
                    'cost_change': f"${projected_cost - current_cost:+.2f}"
                }
            }

            return json.dumps(impact, indent=2)

        except Exception as e:
            return f"Error calculating ROI impact: {str(e)}"

    def list_available_campaigns(self) -> str:
        """
        List all campaigns currently loaded in cache.

        Returns:
            JSON string with campaign list
        """
        campaigns = list(set([key.split('_')[0] for key in self.data_cache.keys()]))

        if not campaigns:
            return "No campaigns loaded. Use load_campaign_data() to load a campaign first."

        result = {
            'loaded_campaigns': campaigns,
            'count': len(campaigns)
        }

        return json.dumps(result, indent=2)

    def get_recommendations_summary(
        self,
        campaign_id: str,
        top_n: int = 3
    ) -> str:
        """
        Get actionable recommendations for campaign optimization.

        Args:
            campaign_id: Campaign identifier
            top_n: Number of top recommendations to return

        Returns:
            Human-readable recommendations
        """
        try:
            # Parse inputs
            if isinstance(top_n, str):
                top_n = int(top_n)
            # Get segments
            cache_key = f"{campaign_id}_segments"
            if cache_key not in self.analysis_cache:
                self.run_segmentation_analysis(campaign_id)

            segments = self.analysis_cache[cache_key]

            if not segments:
                return "No recommendations available. No significant segments found."

            top_segments = segments[:top_n]

            recommendations = []
            for i, seg in enumerate(top_segments, 1):
                bid_change = (seg['bid_multiplier'] - 1) * 100
                action = "INCREASE" if bid_change > 0 else "DECREASE"

                rec = (
                    f"\n{i}. {action} BIDS for {seg['condition']}\n"
                    f"   Current eCR: {seg['ecr']:.2%} (baseline lift: {seg['ecr_lift']:+.1%})\n"
                    f"   Recommended bid adjustment: {bid_change:+.0f}% (multiplier: {seg['bid_multiplier']:.2f}x)\n"
                    f"   Segment size: {seg['sessions']:,} sessions\n"
                    f"   Confidence: {seg['confidence_score']:.0%}\n"
                    f"   Statistical significance: Cramér's V = {seg['feature_importance']:.3f}"
                )
                recommendations.append(rec)

            summary = (
                f"TOP {top_n} OPTIMIZATION RECOMMENDATIONS FOR {campaign_id.upper()}\n"
                f"{'=' * 70}\n"
                f"{''.join(recommendations)}\n"
                f"\nTo see more segments, use run_segmentation_analysis() with max_segments parameter."
            )

            return summary

        except Exception as e:
            return f"Error generating recommendations: {str(e)}"


# Singleton instance
_tools_instance = None

def get_tools_instance() -> CampaignAnalysisTools:
    """Get or create the singleton tools instance."""
    global _tools_instance
    if _tools_instance is None:
        _tools_instance = CampaignAnalysisTools()
    return _tools_instance
